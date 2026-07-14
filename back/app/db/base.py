from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.core.config import settings


class BaseModel(DeclarativeBase):

    @declared_attr.directive
    def __table_args__(cls):
        return {
            "schema": settings.core_schema
        }