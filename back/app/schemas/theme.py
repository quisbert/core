import uuid

from pydantic import BaseModel, ConfigDict


class ThemeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    name: str
    description: str | None
    type: str

    sidebar_background_color: str
    sidebar_foreground_color: str

    topbar_background_color: str
    topbar_foreground_color: str

    card_header_background_color: str
    card_header_foreground_color: str

    table_header_background_color: str
    table_header_foreground_color: str

    border_color: str

    is_default: bool
    is_active: bool


class ThemeUpdateRequest(BaseModel):
    sidebar_background_color: str
    sidebar_foreground_color: str

    topbar_background_color: str
    topbar_foreground_color: str

    card_header_background_color: str
    card_header_foreground_color: str

    table_header_background_color: str
    table_header_foreground_color: str

    border_color: str