from typing import TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse


T = TypeVar("T")


def paginate(
    db: Session,
    statement: Select,
    page: int,
    page_size: int,
) -> PaginatedResponse[T]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    count_statement = select(
        func.count()
    ).select_from(
        statement.order_by(None).subquery()
    )

    total = db.scalar(count_statement) or 0

    items = list(
        db.scalars(
            statement
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).all()
    )

    return PaginatedResponse.create(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
    )