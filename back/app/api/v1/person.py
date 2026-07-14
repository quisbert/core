from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, require_permission
from app.db.database import get_db
from app.schemas.person import (
    PersonCreate,
    PersonResponse,
    PersonUpdate,
)
from app.services.person_service import (
    PersonError,
    create_person,
    delete_person,
    get_people,
    get_person,
    update_person,
)

from app.schemas.pagination import PaginatedResponse

router = APIRouter(
    prefix="/people",
    tags=["People"],
)

@router.get(
    "",
    response_model=PaginatedResponse[PersonResponse],
    dependencies=[
        Depends(require_permission("people.read"))
    ],
)
def index(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=150),
    is_active: bool | None = Query(default=None),
):
    return get_people(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        is_active=is_active,
    )

@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    dependencies=[Depends(require_permission("people.read"))],
)
def show(
    person_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):

    person = get_person(db, person_id)

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found.",
        )

    return person


@router.post(
    "",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("people.create"))],
)
def store(
    payload: PersonCreate,
    db: Annotated[Session, Depends(get_db)],
):

    try:
        return create_person(db, payload)

    except PersonError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.put(
    "/{person_id}",
    response_model=PersonResponse,
    dependencies=[Depends(require_permission("people.update"))],
)
def update(
    person_id: UUID,
    payload: PersonUpdate,
    db: Annotated[Session, Depends(get_db)],
):

    person = get_person(db, person_id)

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found.",
        )

    try:
        return update_person(
            db=db,
            person=person,
            data=payload,
        )

    except PersonError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("people.delete"))],
)
def destroy(
    person_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):

    person = get_person(db, person_id)

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found.",
        )

    delete_person(
        db=db,
        person=person,
        deleted_by=current_user.id,
    )