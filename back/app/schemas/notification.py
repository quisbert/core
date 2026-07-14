from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificationCreate(BaseModel):
    title: str
    message: str

    priority: str = "NORMAL"

    entity_table: str | None = None
    entity_id: UUID | None = None

    expires_at: datetime | None = None

    requires_response: bool = False

    users: list[UUID]


class NotificationUpdate(BaseModel):
    title: str | None = None
    message: str | None = None

    priority: str | None = None

    status: str | None = None

    expires_at: datetime | None = None

    requires_response: bool | None = None

    is_active: bool | None = None


class NotificationReply(BaseModel):
    reply: str


class NotificationResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    title: str
    message: str

    priority: str
    status: str

    entity_table: str | None
    entity_id: UUID | None

    requires_response: bool

    expires_at: datetime | None

    created_at: datetime