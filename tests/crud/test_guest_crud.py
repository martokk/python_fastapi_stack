from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session

from app import crud, models
from tests.mock_objects import MOCKED_GUEST_1, MOCKED_GUESTS


async def get_mocked_guest(db: Session) -> models.Guest:
    """
    Create a mocked guest.
    """
    # Create an guest with an owner
    owner = await crud.user.get(db=db, username="test_user")
    guest_create = models.GuestCreate(**MOCKED_GUEST_1)

    return await crud.guest.create_with_owner_id(db=db, obj_in=guest_create, owner_id=owner.id)


async def test_create_guest(db_with_user: Session) -> None:
    """
    Test creating a new guest with an owner.
    """
    created_guest = await get_mocked_guest(db=db_with_user)

    # Check the guest was created
    assert created_guest.title == MOCKED_GUEST_1["title"]
    assert created_guest.description == MOCKED_GUEST_1["description"]
    assert created_guest.owner_id is not None


async def test_get_guest(db_with_user: Session) -> None:
    """
    Test getting an guest by id.
    """
    created_guest = await get_mocked_guest(db=db_with_user)

    # Get the guest
    db_guest = await crud.guest.get(db=db_with_user, id=created_guest.id)
    assert db_guest
    assert db_guest.id == created_guest.id
    assert db_guest.title == created_guest.title
    assert db_guest.description == created_guest.description
    assert db_guest.owner_id == created_guest.owner_id


async def test_update_guest(db_with_user: Session) -> None:
    """
    Test updating an guest.
    """
    created_guest = await get_mocked_guest(db=db_with_user)

    # Update the guest
    db_guest = await crud.guest.get(db=db_with_user, id=created_guest.id)
    db_guest_update = models.GuestUpdate(description="New Description")
    updated_guest = await crud.guest.update(
        db=db_with_user, id=created_guest.id, obj_in=db_guest_update
    )
    assert db_guest.id == updated_guest.id
    assert db_guest.title == updated_guest.title
    assert updated_guest.description == "New Description"
    assert db_guest.owner_id == updated_guest.owner_id


async def test_update_guest_without_filter(db_with_user: Session) -> None:
    """
    Test updating an guest without a filter.
    """
    created_guest = await get_mocked_guest(db=db_with_user)

    # Update the guest (without a filter)
    await crud.guest.get(db=db_with_user, id=created_guest.id)
    db_guest_update = models.GuestUpdate(description="New Description")
    with pytest.raises(ValueError):
        await crud.guest.update(db=db_with_user, obj_in=db_guest_update)


async def test_delete_guest(db_with_user: Session) -> None:
    """
    Test deleting an guest.
    """
    created_guest = await get_mocked_guest(db=db_with_user)

    # Delete the guest
    await crud.guest.remove(db=db_with_user, id=created_guest.id)
    with pytest.raises(crud.RecordNotFoundError):
        await crud.guest.get(db=db_with_user, id=created_guest.id)


async def test_delete_guest_delete_error(db_with_user: Session, mocker: MagicMock) -> None:
    """
    Test deleting an guest with a delete error.
    """
    mocker.patch("app.crud.guest.get", return_value=None)
    with pytest.raises(crud.DeleteError):
        await crud.guest.remove(db=db_with_user, id="00000001")


async def test_get_all_guests(db_with_user: Session) -> None:
    """
    Test getting all guests.
    """
    # Create some guests
    for i, guest in enumerate(MOCKED_GUESTS):
        guest_create = models.GuestCreate(**guest)
        await crud.guest.create_with_owner_id(
            db=db_with_user, obj_in=guest_create, owner_id=f"0000000{i}"
        )

    # Get all guests
    guests = await crud.guest.get_all(db=db_with_user)
    assert len(guests) == len(MOCKED_GUESTS)
