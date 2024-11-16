from fastapi.testclient import TestClient
from sqlmodel import Session

from app import settings
from tests.mock_objects import MOCKED_GUEST_1, MOCKED_GUESTS


def test_create_guest(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can create a new guest.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 201
    guest = response.json()
    assert guest["title"] == MOCKED_GUEST_1["title"]
    assert guest["description"] == MOCKED_GUEST_1["description"]
    assert guest["url"] == MOCKED_GUEST_1["url"]
    assert guest["owner_id"] is not None
    assert guest["id"] is not None


def test_create_duplicate_guest(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """
    Test a duplicate guest cannot be created.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 201

    # Try to create a duplicate guest
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 200
    duplicate = response.json()
    assert duplicate["detail"] == "Guest already exists"


def test_read_guest(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can read an guest.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 201
    created_guest = response.json()

    # Read Guest
    response = client.get(
        f"{settings.API_V1_PREFIX}/guest/{created_guest['id']}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    read_guest = response.json()

    assert read_guest["title"] == MOCKED_GUEST_1["title"]
    assert read_guest["description"] == MOCKED_GUEST_1["description"]
    assert read_guest["url"] == MOCKED_GUEST_1["url"]
    assert read_guest["owner_id"] is not None
    assert read_guest["id"] is not None


def test_get_guest_not_found(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a guest not found error is returned.
    """
    response = client.get(
        f"{settings.API_V1_PREFIX}/guest/1",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Guest not found"


def test_get_guest_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.get(
        f"{settings.API_V1_PREFIX}/guest/5kwf8hFn",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_superuser_get_all_guests(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    """
    Test that a superuser can get all guests.
    """

    # Create 3 guests
    for guest in MOCKED_GUESTS:
        response = client.post(
            f"{settings.API_V1_PREFIX}/guest/",
            headers=superuser_token_headers,
            json=guest,
        )
        assert response.status_code == 201

    # Get all guests as superuser
    response = client.get(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    guests = response.json()
    assert len(guests) == 3


def test_normal_user_get_all_guests(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
) -> None:
    """
    Test that a normal user can get all their own guests.
    """
    # Create 2 guests as normal user
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=normal_user_token_headers,
        json=MOCKED_GUESTS[0],
    )
    assert response.status_code == 201
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=normal_user_token_headers,
        json=MOCKED_GUESTS[1],
    )
    assert response.status_code == 201

    # Create 1 guest as super user
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUESTS[2],
    )
    assert response.status_code == 201

    # Get all guests as normal user
    response = client.get(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    guests = response.json()
    assert len(guests) == 2


def test_update_guest(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can update an guest.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 201
    created_guest = response.json()

    # Update Guest
    update_data = MOCKED_GUEST_1.copy()
    update_data["title"] = "Updated Title"
    response = client.patch(
        f"{settings.API_V1_PREFIX}/guest/{created_guest['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    updated_guest = response.json()
    assert updated_guest["title"] == update_data["title"]

    # Update wrong guest
    response = client.patch(
        f"{settings.API_V1_PREFIX}/guest/99999",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 404


def test_update_guest_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.patch(
        f"{settings.API_V1_PREFIX}/guest/5kwf8hFn",
        headers=normal_user_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_guest(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can delete an guest.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/guest/",
        headers=superuser_token_headers,
        json=MOCKED_GUEST_1,
    )
    assert response.status_code == 201
    created_guest = response.json()

    # Delete Guest
    response = client.delete(
        f"{settings.API_V1_PREFIX}/guest/{created_guest['id']}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Delete wrong guest
    response = client.delete(
        f"{settings.API_V1_PREFIX}/guest/99999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_delete_guest_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.delete(
        f"{settings.API_V1_PREFIX}/guest/5kwf8hFn",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"
