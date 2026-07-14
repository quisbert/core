from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    CurrentUser,
    require_permission,
)
from app.db.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationReply,
    NotificationResponse,
    NotificationUpdate,
)
from app.schemas.notification_user import (
    NotificationInbox,
    NotificationMessage,
    NotificationUnread,
)
from app.services.notification_service import (
    NotificationError,
    create_notification,
    delete_notification,
    get_notification,
    inbox,
    mark_as_read,
    reply_notification,
    unread_count,
    update_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/inbox",
    response_model=list[NotificationInbox],
    dependencies=[
        Depends(require_permission("notifications.read"))
    ],
)
def get_inbox(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    rows = inbox(
        db=db,
        user_id=current_user.id,
    )

    return [
        NotificationInbox(
            notification_id=notification.id,
            title=notification.title,
            message=notification.message,
            priority=notification.priority,
            status=relation.status,
            sent_at=relation.sent_at,
            read_at=relation.read_at,
            requires_response=notification.requires_response,
            entity_table=notification.entity_table,
            entity_id=notification.entity_id,
        )
        for relation, notification in rows
    ]


@router.get(
    "/unread-count",
    response_model=NotificationUnread,
    dependencies=[
        Depends(require_permission("notifications.read"))
    ],
)
def get_unread_count(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    return NotificationUnread(
        count=unread_count(
            db=db,
            user_id=current_user.id,
        )
    )


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("notifications.create"))
    ],
)
def store(
    payload: NotificationCreate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        return create_notification(
            db=db,
            data=payload,
            created_by=current_user.id,
        )

    except NotificationError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationMessage,
    dependencies=[
        Depends(require_permission("notifications.read"))
    ],
)
def read(
    notification_id: UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        mark_as_read(
            db=db,
            notification_id=notification_id,
            user_id=current_user.id,
        )

        return NotificationMessage(
            message="Notification marked as read."
        )

    except NotificationError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.patch(
    "/{notification_id}/reply",
    response_model=NotificationMessage,
    dependencies=[
        Depends(require_permission("notifications.reply"))
    ],
)
def reply(
    notification_id: UUID,
    payload: NotificationReply,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    try:

        reply_notification(
            db=db,
            notification_id=notification_id,
            user_id=current_user.id,
            data=payload,
        )

        return NotificationMessage(
            message="Reply sent successfully."
        )

    except NotificationError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    dependencies=[
        Depends(require_permission("notifications.update"))
    ],
)
def update(
    notification_id: UUID,
    payload: NotificationUpdate,
    db: Annotated[Session, Depends(get_db)],
):

    notification = get_notification(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:

        raise HTTPException(
            status_code=404,
            detail="Notification not found.",
        )

    return update_notification(
        db=db,
        notification=notification,
        data=payload,
    )


@router.delete(
    "/{notification_id}",
    response_model=NotificationMessage,
    dependencies=[
        Depends(require_permission("notifications.delete"))
    ],
)
def destroy(
    notification_id: UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    notification = get_notification(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:

        raise HTTPException(
            status_code=404,
            detail="Notification not found.",
        )

    delete_notification(
        db=db,
        notification=notification,
        deleted_by=current_user.id,
    )

    return NotificationMessage(
        message="Notification deleted successfully."
    )