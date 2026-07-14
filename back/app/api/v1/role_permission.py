from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_permission
from app.db.database import get_db
from app.schemas.role_permission import (
    RolePermissionCreate,
    RolePermissionResponse,
)
from app.services.role_permission_service import (
    RolePermissionError,
    assign_permission,
    get_role_permissions,
    remove_permission,
)

router = APIRouter(
    prefix="/role-permissions",
    tags=["Role Permissions"],
)


@router.get(
    "/{role_id}",
    response_model=list[RolePermissionResponse],
    dependencies=[
        Depends(require_permission("roles.read"))
    ],
)
def index(
    role_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    rows = get_role_permissions(
        db,
        role_id,
    )

    return [
        RolePermissionResponse(
            role_id=rp.role_id,
            permission_id=permission.id,
            permission_code=permission.code,
            permission_name=permission.name,
        )
        for rp, permission in rows
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("roles.update"))
    ],
)
def store(
    payload: RolePermissionCreate,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        assign_permission(
            db=db,
            data=payload,
        )

        return {
            "message": "Permission assigned successfully."
        }

    except RolePermissionError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{role_id}/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("roles.update"))
    ],
)
def destroy(
    role_id: UUID,
    permission_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        remove_permission(
            db=db,
            role_id=role_id,
            permission_id=permission_id,
        )

    except RolePermissionError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )