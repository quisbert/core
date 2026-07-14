from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    code: str
    name: str
    description: str | None = None


class PermissionUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    description: str | None = None
    is_active: bool