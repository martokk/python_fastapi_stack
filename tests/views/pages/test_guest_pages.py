from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Cookies
from sqlmodel import Session

from app import crud, models, settings
from tests.mock_objects import MOCKED_GUEST_1, MOCKED_GUESTS


@pytest.fixture(name="guest_1")
async def fixture_guest_1(db_with_user: Session) -> models.Guest:
    """
    Create an guest for testing.
    """
    user = await crud.user.get(db=db_with_user, username="test_user")
    guest_create = models.GuestCreate(**MOCKED_GUEST_1)
    return await crud.guest.create_with_owner_id(
        db=db_with_user, obj_in=guest_create, owner_id=user.id
    )


@pytest.fixture(name="guests")
async def fixture_guests(db_with_user: Session) -> list[models.Guest]:
    """
    Create an guest for testing.
    """
    # Create 1 as a superuser
    user = await crud.user.get(db=db_with_user, username=settings.FIRST_SUPERUSER_USERNAME)
    guests = []
    guest_create = models.GuestCreate(**MOCKED_GUESTS[0])
    guests.append(
        await crud.guest.create_with_owner_id(
            db=db_with_user, obj_in=guest_create, owner_id=user.id
        )
    )

    # Create 2 as a normal user
    user = await crud.user.get(db=db_with_user, username="test_user")
    for mocked_guest in [MOCKED_GUESTS[1], MOCKED_GUESTS[2]]:
        guest_create = models.GuestCreate(**mocked_guest)
        guests.append(
            await crud.guest.create_with_owner_id(
                db=db_with_user, obj_in=guest_create, owner_id=user.id
            )
        )
    return guests


def test_create_guest_page(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that the create guest page is returned.
    """
    client.cookies = normal_user_cookies
    response = client.get("/guests/create")
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/create.html"  # type: ignore


def test_handle_create_guest(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can create a new guest.
    """
    client.cookies = normal_user_cookies
    response = client.post(
        "/guests/create",
        data=MOCKED_GUEST_1,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/list.html"  # type: ignore


@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
def test_create_duplicate_guest(
    db_with_user: Session,  # pylint: disable=unused-argument
    guest_1: models.Guest,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:  # pytest:
    """
    Test a duplicate guest cannot be created.
    """
    # Try to create a duplicate guest
    with pytest.raises(Exception):
        response = client.post(
            "/guests/create",
            data=MOCKED_GUEST_1,
        )
    # assert response.status_code == status.HTTP_200_OK
    # assert response.template.name == "guest/create.html"  # type: ignore
    # assert response.context["alerts"].danger[0] == "Guest already exists"  # type: ignore


def test_read_guest(
    db_with_user: Session,  # pylint: disable=unused-argument
    guest_1: models.Guest,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can read an guest.
    """
    # Read the guest
    response = client.get(
        f"/guest/{guest_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/view.html"  # type: ignore


def test_get_guest_not_found(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a guest not found error is returned.
    """
    client.cookies = normal_user_cookies

    # Read the guest
    response = client.get("/guest/8675309")
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == "/guests"


def test_get_guest_forbidden(
    db_with_user: Session,  # pylint: disable=unused-argument
    guest_1: models.Guest,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a forbidden error is returned when a user tries to read an guest
    """
    client.cookies = normal_user_cookies

    # Read the guest
    response = client.get(
        f"/guest/{guest_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/view.html"  # type: ignore

    # Logout
    response = client.get(
        "/logout",
    )
    assert response.status_code == status.HTTP_200_OK

    # Attempt Read the guest
    response = client.get(
        f"/guest/{guest_1.id}",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == "/login"  # type: ignore


def test_normal_user_get_all_guests(
    db_with_user: Session,  # pylint: disable=unused-argument
    guests: list[models.Guest],  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
    superuser_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a normal user can get all their own guests.
    """

    # List all guests as normal user
    client.cookies = normal_user_cookies
    response = client.get(
        "/guests",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/list.html"  # type: ignore

    # Assert only 2 guests are returned (not the superuser's guest)
    assert len(response.context["guests"]) == 2  # type: ignore


def test_edit_guest_page(
    db_with_user: Session,  # pylint: disable=unused-argument
    guest_1: models.Guest,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that the edit guest page is returned.
    """
    client.cookies = normal_user_cookies
    response = client.get(
        f"/guest/{guest_1.id}/edit",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/edit.html"  # type: ignore

    # Test invalid guest id
    response = client.get(
        f"/guest/invalid_user_id/edit",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_302_FOUND
    assert response.context["alerts"].danger[0] == "Guest not found"  # type: ignore
    assert response.url.path == "/guests"


def test_update_guest(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    guest_1: models.Guest,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can update an guest.
    """
    client.cookies = normal_user_cookies

    # Update the guest
    response = client.post(
        f"/guest/{guest_1.id}/edit",  # type: ignore
        data=MOCKED_GUESTS[1],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/edit.html"  # type: ignore

    # View the guest
    response = client.get(
        f"/guest/{guest_1.id}",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/view.html"  # type: ignore
    assert response.context["guest"].title == MOCKED_GUESTS[1]["title"]  # type: ignore
    assert response.context["guest"].description == MOCKED_GUESTS[1]["description"]  # type: ignore
    assert response.context["guest"].url == MOCKED_GUESTS[1]["url"]  # type: ignore

    # Test invalid guest id
    response = client.post(
        f"/guest/invalid_user_id/edit",  # type: ignore
        data=MOCKED_GUESTS[1],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.context["alerts"].danger[0] == "Guest not found"  # type: ignore
    assert response.url.path == "/guests"


def test_delete_guest(
    db_with_user: Session,  # pylint: disable=unused-argument
    guest_1: models.Guest,
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can delete an guest.
    """
    client.cookies = normal_user_cookies

    # Delete the guest
    response = client.get(
        f"/guest/{guest_1.id}/delete",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.url.path == "/guests"

    # View the guest
    response = client.get(
        f"/guest/{guest_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.context["alerts"].danger == ["Guest not found"]  # type: ignore

    # Test invalid guest id
    response = client.get(
        f"/guest/invalid_user_id/delete",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.context["alerts"].danger[0] == "Guest not found"  # type: ignore
    assert response.url.path == "/guests"

    # Test DeleteError
    with patch("app.crud.guest.remove", side_effect=crud.DeleteError):
        response = client.get(
            f"/guest/123/delete",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
        assert response.context["alerts"].danger[0] == "Error deleting guest"  # type: ignore


def test_list_all_guests(
    db_with_user: Session,  # pylint: disable=unused-argument
    guests: list[models.Guest],  # pylint: disable=unused-argument
    client: TestClient,
    superuser_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a superuser can get all guests.
    """

    # List all guests as superuser
    client.cookies = superuser_cookies
    response = client.get(
        "/guests/all",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "guest/list.html"  # type: ignore

    # Assert all 3 guests are returned
    assert len(response.context["guests"]) == 3  # type: ignore
