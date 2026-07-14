from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    CurrentUser,
    require_permission,
)
from app.db.database import get_db
from app.schemas.role import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)
from app.services.role_service import (
    RoleError,
    create_role,
    delete_role,
    get_role,
    get_roles,
    update_role,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get(
    "",
    response_model=list[RoleResponse],
    dependencies=[
        Depends(
            require_permission("roles.read")
        )
    ],
)
def index(
    db: Annotated[Session, Depends(get_db)],
    search: str | None = Query(default=None),
):

    return get_roles(
        db=db,
        search=search,
    )


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[
        Depends(
            require_permission("roles.read")
        )
    ],
)
def show(
    role_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    role = get_role(
        db,
        role_id,
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found.",
        )

    return role


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission("roles.create")
        )
    ],
)
def store(
    payload: RoleCreate,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        return create_role(
            db=db,
            data=payload,
        )

    except RoleError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[
        Depends(
            require_permission("roles.update")
        )
    ],
)
def update(
    role_id: UUID,
    payload: RoleUpdate,
    db: Annotated[Session, Depends(get_db)],
):

    role = get_role(
        db,
        role_id,
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found.",
        )

    try:

        return update_role(
            db=db,
            role=role,
            data=payload,
        )

    except RoleError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission("roles.delete")
        )
    ],
)
def destroy(
    role_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):

    role = get_role(
        db,
        role_id,
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found.",
        )

    delete_role(
        db=db,
        role=role,
        deleted_by=current_user.id,
    )