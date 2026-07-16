import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.theme import Theme
from app.schemas.theme import ThemeUpdateRequest


class ThemeError(Exception):
    pass


def get_themes(
    db: Session,
) -> list[Theme]:
    statement = (
        select(Theme)
        .where(
            Theme.deleted_at.is_(None),
            Theme.is_active.is_(True),
        )
        .order_by(
            Theme.is_default.desc(),
            Theme.name.asc(),
        )
    )

    return list(
        db.scalars(statement).all()
    )


def get_theme(
    db: Session,
    theme_id: uuid.UUID,
) -> Theme | None:
    statement = select(Theme).where(
        Theme.id == theme_id,
        Theme.deleted_at.is_(None),
        Theme.is_active.is_(True),
    )

    return db.scalar(statement)


def get_institutional_theme(
    db: Session,
) -> Theme | None:
    statement = select(Theme).where(
        Theme.type == "INSTITUTIONAL",
        Theme.deleted_at.is_(None),
        Theme.is_active.is_(True),
    )

    return db.scalar(statement)


def update_theme(
    db: Session,
    theme: Theme,
    data: ThemeUpdateRequest,
) -> Theme:
    if theme.type != "INSTITUTIONAL":
        raise ThemeError(
            "The default theme cannot be modified."
        )

    values = data.model_dump(
        exclude_unset=True,
    )

    for field, value in values.items():
        setattr(theme, field, value)

    db.commit()
    db.refresh(theme)

    return theme