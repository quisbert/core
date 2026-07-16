from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization_setting import OrganizationSetting
from app.models.theme import Theme


def run(db: Session) -> None:

    exists = db.scalar(
        select(OrganizationSetting)
    )

    if exists:
        return

    theme = db.scalar(
        select(Theme).where(
            Theme.type == "INSTITUTIONAL"
        )
    )

    if theme is None:
        raise RuntimeError(
            "Institutional theme not found."
        )

    db.add(
        OrganizationSetting(
            organization_name="Core API",
            organization_abbreviation="CORE",

            system_name="Core API",
            system_abbreviation="CORE",

            email=None,
            phone=None,
            website=None,
            address=None,

            timezone="America/La_Paz",
            language="es",

            login_message="Welcome to Core API.",

            theme_id=theme.id,
        )
    )

    db.commit()