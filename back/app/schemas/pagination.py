import math
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int
    pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(
        cls,
        items: list[T],
        page: int,
        page_size: int,
        total: int,
    ):
        pages = math.ceil(total / page_size) if total else 0

        return cls(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_previous=page > 1,
        )