from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import (
    CurrentUser,
    require_permission,
)
from app.db.database import get_db
from app.schemas.profile import (
    ChangePasswordRequest,
    ProfileResponse,
    ProfileUpdate,
)
from app.services.profile_service import (
    ProfileError,
    change_password,
    update_profile,
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get(
    "",
    response_model=ProfileResponse,
    dependencies=[
        Depends(require_permission("profile.read"))
    ],
)
def show(
    current_user: CurrentUser,
):

    person = current_user.person

    return ProfileResponse(
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        second_last_name=person.second_last_name,
        phone=person.phone,
        mobile=person.mobile,
        address=person.address,
    )


@router.put(
    "",
    response_model=ProfileResponse,
    dependencies=[
        Depends(require_permission("profile.update"))
    ],
)
def update(
    payload: ProfileUpdate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    user = update_profile(
        db=db,
        user=current_user,
        data=payload,
    )

    person = user.person

    return ProfileResponse(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        second_last_name=person.second_last_name,
        phone=person.phone,
        mobile=person.mobile,
        address=person.address,
    )


@router.put(
    "/change-password",
    dependencies=[
        Depends(require_permission("profile.change_password"))
    ],
)
def password(
    payload: ChangePasswordRequest,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        change_password(
            db=db,
            user=current_user,
            data=payload,
        )

        return {
            "message": "Password changed successfully."
        }

    except ProfileError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )