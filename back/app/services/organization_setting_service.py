import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.organization_setting import OrganizationSetting
from app.models.theme import Theme
from app.schemas.organization_setting import (
    OrganizationSettingUpdateRequest,
)


class OrganizationSettingError(Exception):
    pass


def get_organization_setting(
    db: Session,
) -> OrganizationSetting | None:
    statement = (
        select(OrganizationSetting)
        .where(
            OrganizationSetting.deleted_at.is_(None),
            OrganizationSetting.is_active.is_(True),
        )
        .limit(1)
    )

    return db.scalar(statement)


def _validate_theme(
    db: Session,
    theme_id: uuid.UUID,
) -> Theme:
    theme = db.scalar(
        select(Theme).where(
            Theme.id == theme_id,
            Theme.deleted_at.is_(None),
            Theme.is_active.is_(True),
        )
    )

    if theme is None:
        raise OrganizationSettingError(
            "Theme not found."
        )

    return theme


def _validate_file(
    db: Session,
    file_id: uuid.UUID | None,
    field_name: str,
) -> None:
    if file_id is None:
        return

    file = db.scalar(
        select(File).where(
            File.id == file_id,
            File.deleted_at.is_(None),
            File.is_active.is_(True),
        )
    )

    if file is None:
        raise OrganizationSettingError(
            f"Invalid {field_name} file."
        )


def update_organization_setting(
    db: Session,
    setting: OrganizationSetting,
    data: OrganizationSettingUpdateRequest,
) -> OrganizationSetting:
    _validate_theme(
        db=db,
        theme_id=data.theme_id,
    )

    _validate_file(
        db=db,
        file_id=data.logo_id,
        field_name="logo",
    )

    _validate_file(
        db=db,
        file_id=data.favicon_id,
        field_name="favicon",
    )

    _validate_file(
        db=db,
        file_id=data.login_background_id,
        field_name="login background",
    )

    values = data.model_dump(
        exclude_unset=True,
    )

    for field, value in values.items():
        setattr(setting, field, value)

    db.commit()
    db.refresh(setting)

    return setting