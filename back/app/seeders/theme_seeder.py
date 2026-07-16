from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.theme import Theme


def run(db: Session) -> None:

    data = [
        {
            "name": "Default",
            "description": "Default Core API theme.",
            "type": "DEFAULT",
            "sidebar_background_color": "#18181B",
            "sidebar_foreground_color": "#FAFAFA",
            "topbar_background_color": "#FFFFFF",
            "topbar_foreground_color": "#18181B",
            "card_header_background_color": "#F4F4F5",
            "card_header_foreground_color": "#18181B",
            "table_header_background_color": "#F4F4F5",
            "table_header_foreground_color": "#18181B",
            "border_color": "#E4E4E7",
            "is_default": True,
        },
        {
            "name": "Institutional",
            "description": "Institutional customizable theme.",
            "type": "INSTITUTIONAL",
            "sidebar_background_color": "#18181B",
            "sidebar_foreground_color": "#FAFAFA",
            "topbar_background_color": "#FFFFFF",
            "topbar_foreground_color": "#18181B",
            "card_header_background_color": "#F4F4F5",
            "card_header_foreground_color": "#18181B",
            "table_header_background_color": "#F4F4F5",
            "table_header_foreground_color": "#18181B",
            "border_color": "#E4E4E7",
            "is_default": False,
        },
    ]

    for item in data:

        exists = db.scalar(
            select(Theme).where(
                Theme.type == item["type"]
            )
        )

        if exists:
            continue

        db.add(
            Theme(**item)
        )

    db.commit()