from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, require_permission
from app.db.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import (
    UserError,
    create_user,
    delete_user,
    get_user,
    get_users,
    reset_user_password,
    unlock_user,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(require_permission("users.read"))],
)
def index(
    db: Annotated[Session, Depends(get_db)],
    search: str | None = Query(default=None),
):
    return get_users(db, search)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.read"))],
)
def show(
    user_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("users.create"))],
)
def store(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return create_user(db, payload)

    except UserError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.update"))],
)
def update(
    user_id: UUID,
    payload: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    try:
        return update_user(
            db=db,
            user=user,
            data=payload,
            updated_by=current_user.id,
        )

    except UserError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("users.delete"))],
)
def destroy(
    user_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    delete_user(
        db=db,
        user=user,
        deleted_by=current_user.id,
    )


@router.patch(
    "/{user_id}/unlock",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.unlock"))],
)
def unlock(
    user_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return unlock_user(
        db=db,
        user=user,
        updated_by=current_user.id,
    )


@router.patch(
    "/{user_id}/reset-password",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.reset_password"))],
)
def reset_password(
    user_id: UUID,
    password: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return reset_user_password(
        db=db,
        user=user,
        password=password,
        updated_by=current_user.id,
    )