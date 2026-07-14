from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    CurrentUser,
    require_permission,
)
from app.db.database import get_db
from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from app.services.permission_service import (
    PermissionError,
    create_permission,
    delete_permission,
    get_permission,
    get_permissions,
    update_permission,
)

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.get(
    "",
    response_model=list[PermissionResponse],
    dependencies=[
        Depends(
            require_permission("permissions.read")
        )
    ],
)
def index(
    db: Annotated[Session, Depends(get_db)],
    search: str | None = Query(default=None),
):

    return get_permissions(
        db=db,
        search=search,
    )


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    dependencies=[
        Depends(
            require_permission("permissions.read")
        )
    ],
)
def show(
    permission_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    permission = get_permission(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found.",
        )

    return permission


@router.post(
    "",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission("permissions.create")
        )
    ],
)
def store(
    payload: PermissionCreate,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        return create_permission(
            db=db,
            data=payload,
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
    dependencies=[
        Depends(
            require_permission("permissions.update")
        )
    ],
)
def update(
    permission_id: UUID,
    payload: PermissionUpdate,
    db: Annotated[Session, Depends(get_db)],
):

    permission = get_permission(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found.",
        )

    try:

        return update_permission(
            db=db,
            permission=permission,
            data=payload,
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission("permissions.delete")
        )
    ],
)
def destroy(
    permission_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):

    permission = get_permission(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found.",
        )

    delete_permission(
        db=db,
        permission=permission,
        deleted_by=current_user.id,
    )