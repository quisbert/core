from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationInbox(BaseModel):

    notification_id: UUID

    title: str
    message: str

    priority: str
    status: str

    sent_at: datetime
    read_at: datetime | None

    requires_response: bool

    entity_table: str | None
    entity_id: UUID | None


class NotificationUnread(BaseModel):
    count: int


class NotificationMessage(BaseModel):
    message: str