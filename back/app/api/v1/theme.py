import uuid
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.theme import (
    ThemeResponse,
    ThemeUpdateRequest,
)

from app.services.theme_service import (
    ThemeError,
    get_theme,
    get_themes,
    update_theme,
)

router = APIRouter(
    prefix="/themes",
    tags=["Themes"],
)


@router.get(
    "",
    response_model=list[ThemeResponse],
)
def read_themes(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):

    return get_themes(db)


@router.get(
    "/{theme_id}",
    response_model=ThemeResponse,
)
def read_theme(
    theme_id: uuid.UUID,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):

    theme = get_theme(
        db=db,
        theme_id=theme_id,
    )

    if theme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found.",
        )

    return theme


@router.put(
    "/{theme_id}",
    response_model=ThemeResponse,
)
def update_theme_endpoint(
    theme_id: uuid.UUID,
    payload: ThemeUpdateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):

    theme = get_theme(
        db=db,
        theme_id=theme_id,
    )

    if theme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found.",
        )

    try:
        return update_theme(
            db=db,
            theme=theme,
            data=payload,
        )

    except ThemeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )