import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate
from app.schemas.pagination import PaginatedResponse
from app.utils.pagination import paginate


class PersonError(Exception):
    pass

def get_people(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
) -> PaginatedResponse[Person]:
    statement = select(Person).where(
        Person.deleted_at.is_(None)
    )

    if search:
        search_value = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                Person.first_name.ilike(search_value),
                Person.middle_name.ilike(search_value),
                Person.last_name.ilike(search_value),
                Person.second_last_name.ilike(search_value),
                Person.document_number.ilike(search_value),
                Person.email.ilike(search_value),
            )
        )

    if is_active is not None:
        statement = statement.where(
            Person.is_active.is_(is_active)
        )

    statement = statement.order_by(
        Person.first_name.asc(),
        Person.last_name.asc(),
    )

    return paginate(
        db=db,
        statement=statement,
        page=page,
        page_size=page_size,
    )

def get_person(
    db: Session,
    person_id: uuid.UUID,
) -> Person | None:

    statement = (
        select(Person)
        .where(
            Person.id == person_id,
            Person.deleted_at.is_(None),
        )
    )

    return db.scalar(statement)

def create_person(
    db: Session,
    data: PersonCreate,
) -> Person:

    exists = db.scalar(
        select(Person).where(
            Person.document_type_id == data.document_type_id,
            Person.document_number == data.document_number,
            Person.deleted_at.is_(None),
        )
    )

    if exists:
        raise PersonError(
            "Document already exists."
        )

    person = Person(**data.model_dump())

    db.add(person)
    db.commit()
    db.refresh(person)

    return person

def update_person(
    db: Session,
    person: Person,
    data: PersonUpdate,
) -> Person:

    values = data.model_dump(
        exclude_unset=True,
    )

    if "document_number" in values or "document_type_id" in values:

        document_type = values.get(
            "document_type_id",
            person.document_type_id,
        )

        document_number = values.get(
            "document_number",
            person.document_number,
        )

        exists = db.scalar(
            select(Person).where(
                Person.id != person.id,
                Person.document_type_id == document_type,
                Person.document_number == document_number,
                Person.deleted_at.is_(None),
            )
        )

        if exists:
            raise PersonError(
                "Document already exists."
            )

    for key, value in values.items():
        setattr(person, key, value)

    db.commit()
    db.refresh(person)

    return person

def delete_person(
    db: Session,
    person: Person,
    deleted_by: uuid.UUID,
) -> None:

    person.deleted_at = datetime.now(
        timezone.utc
    )

    person.deleted_by = deleted_by
    person.is_active = False

    db.commit()