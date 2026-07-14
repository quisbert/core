from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_permission
from app.db.database import get_db
from app.schemas.user_role import (
    UserRoleCreate,
    UserRoleResponse,
)
from app.services.user_role_service import (
    UserRoleError,
    assign_role,
    get_user_roles,
    remove_role,
)

router = APIRouter(
    prefix="/user-roles",
    tags=["User Roles"],
)


@router.get(
    "/{user_id}",
    response_model=list[UserRoleResponse],
    dependencies=[
        Depends(require_permission("users.read"))
    ],
)
def index(
    user_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    rows = get_user_roles(
        db,
        user_id,
    )

    return [
        UserRoleResponse(
            user_id=ur.user_id,
            role_id=role.id,
            role_code=role.code,
            role_name=role.name,
        )
        for ur, role in rows
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("users.update"))
    ],
)
def store(
    payload: UserRoleCreate,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        assign_role(
            db=db,
            data=payload,
        )

        return {
            "message": "Role assigned successfully."
        }

    except UserRoleError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{user_id}/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("users.update"))
    ],
)
def destroy(
    user_id: UUID,
    role_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        remove_role(
            db=db,
            user_id=user_id,
            role_id=role_id,
        )

    except UserRoleError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )