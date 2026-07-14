from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    person_id: UUID
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_locked: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    person_id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_locked: bool