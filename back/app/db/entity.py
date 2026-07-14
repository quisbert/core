from app.db.base import BaseModel
from app.db.mixins import AuditMixin
from app.db.mixins import SoftDeleteMixin
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class BaseEntity(
    BaseModel,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    __abstract__ = True