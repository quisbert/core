from uuid import UUID

from pydantic import BaseModel


class UserRoleCreate(BaseModel):
    user_id: UUID
    role_id: UUID


class UserRoleResponse(BaseModel):
    user_id: UUID
    role_id: UUID
    role_code: str
    role_name: str