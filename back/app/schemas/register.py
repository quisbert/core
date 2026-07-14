from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID


# -------------------------
# PERSON
# -------------------------

class PersonRegister(BaseModel):

    first_name: str = Field(min_length=2, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)

    last_name: str = Field(min_length=2, max_length=100)
    second_last_name: str | None = Field(default=None, max_length=100)

    birth_date: date | None = None

    document_type_id: UUID
    document_number: str = Field(min_length=1, max_length=30)

    gender_id: UUID | None = None

    email: EmailStr | None = None

    phone: str | None = Field(default=None, max_length=30)
    mobile: str | None = Field(default=None, max_length=30)

    address: str | None = Field(default=None, max_length=255)


# -------------------------
# USER
# -------------------------

class UserRegister(BaseModel):

    username: str = Field(min_length=4, max_length=50)

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# -------------------------
# REQUEST
# -------------------------

class RegisterRequest(BaseModel):

    person: PersonRegister
    user: UserRegister


# -------------------------
# RESPONSE
# -------------------------

class RegisterResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    username: str

    email: EmailStr

    is_active: bool