import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class OrganizationSettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    organization_name: str
    organization_abbreviation: str | None

    system_name: str
    system_abbreviation: str | None

    logo_id: uuid.UUID | None
    favicon_id: uuid.UUID | None
    login_background_id: uuid.UUID | None

    email: EmailStr | None
    phone: str | None
    website: str | None
    address: str | None

    timezone: str
    language: str

    login_message: str | None

    theme_id: uuid.UUID

    is_active: bool


class OrganizationSettingUpdateRequest(BaseModel):
    organization_name: str
    organization_abbreviation: str | None

    system_name: str
    system_abbreviation: str | None

    logo_id: uuid.UUID | None
    favicon_id: uuid.UUID | None
    login_background_id: uuid.UUID | None

    email: EmailStr | None
    phone: str |None
    website: str | None
    address: str | None

    timezone: str
    language: str

    login_message: str | None

    theme_id: uuid.UUID