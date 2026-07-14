from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class PersonBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    second_last_name: str | None = None
    birth_date: date | None = None

    document_type_id: UUID
    document_number: str

    gender_id: UUID | None = None

    email: EmailStr | None = None
    phone: str | None = None
    mobile: str | None = None
    address: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None
    birth_date: date | None = None

    document_type_id: UUID | None = None
    document_number: str | None = None

    gender_id: UUID | None = None

    email: EmailStr | None = None
    phone: str | None = None
    mobile: str | None = None
    address: str | None = None

    is_active: bool | None = None


class PersonResponse(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    is_active: bool