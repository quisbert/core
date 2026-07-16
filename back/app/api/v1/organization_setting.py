import uuid
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.organization_setting import (
    OrganizationSettingResponse,
    OrganizationSettingUpdateRequest,
)

from app.services.organization_setting_service import (
    OrganizationSettingError,
    get_organization_setting,
    update_organization_setting,
)

router = APIRouter(
    prefix="/organization-settings",
    tags=["Organization Settings"],
)


@router.get(
    "",
    response_model=OrganizationSettingResponse,
)
def read_organization_setting(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):

    organization = get_organization_setting(
        db,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization settings not found.",
        )

    return organization


@router.put(
    "",
    response_model=OrganizationSettingResponse,
)
def update_organization_setting_endpoint(
    payload: OrganizationSettingUpdateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):

    organization = get_organization_setting(
        db,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization settings not found.",
        )

    try:
        return update_organization_setting(
            db=db,
            setting=organization,
            data=payload,
        )

    except OrganizationSettingError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )