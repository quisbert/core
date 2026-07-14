from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    is_active: bool

    first_name: str
    middle_name: str | None = None
    last_name: str
    second_last_name: str | None = None

    phone: str | None = None
    mobile: str | None = None
    address: str | None = None


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None

    phone: str | None = None
    mobile: str | None = None
    address: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str