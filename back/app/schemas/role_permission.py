from uuid import UUID

from pydantic import BaseModel


class RolePermissionCreate(BaseModel):
    role_id: UUID
    permission_id: UUID


class RolePermissionResponse(BaseModel):
    role_id: UUID
    permission_id: UUID
    permission_code: str
    permission_name: str