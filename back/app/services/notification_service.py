import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.notification_user import NotificationUser
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationReply,
    NotificationUpdate,
)


class NotificationError(Exception):
    pass


def get_notification(
    db: Session,
    notification_id: uuid.UUID,
) -> Notification | None:

    statement = select(Notification).where(
        Notification.id == notification_id,
        Notification.deleted_at.is_(None),
    )

    return db.scalar(statement)


def create_notification(
    db: Session,
    data: NotificationCreate,
    created_by: uuid.UUID,
) -> Notification:

    users = db.scalars(
        select(User).where(
            User.id.in_(data.users),
            User.deleted_at.is_(None),
            User.is_active.is_(True),
        )
    ).all()

    if not users:
        raise NotificationError(
            "No valid users selected."
        )

    notification = Notification(
        title=data.title,
        message=data.message,
        priority=data.priority,
        status="PENDING",
        entity_table=data.entity_table,
        entity_id=data.entity_id,
        expires_at=data.expires_at,
        requires_response=data.requires_response,
        created_by=created_by,
    )

    db.add(notification)
    db.flush()

    now = datetime.now(timezone.utc)

    for user in users:

        db.add(
            NotificationUser(
                notification_id=notification.id,
                user_id=user.id,
                sent_at=now,
                status="PENDING",
                created_by=created_by,
            )
        )

    db.commit()
    db.refresh(notification)

    return notification


def inbox(
    db: Session,
    user_id: uuid.UUID,
):

    statement = (
        select(
            NotificationUser,
            Notification,
        )
        .join(
            Notification,
            Notification.id == NotificationUser.notification_id,
        )
        .where(
            NotificationUser.user_id == user_id,
            NotificationUser.deleted_at.is_(None),
            Notification.deleted_at.is_(None),
        )
        .order_by(
            NotificationUser.sent_at.desc(),
        )
    )

    return db.execute(statement).all()


def mark_as_read(
    db: Session,
    notification_id: uuid.UUID,
    user_id: uuid.UUID,
) -> NotificationUser:

    relation = db.scalar(
        select(NotificationUser).where(
            NotificationUser.notification_id == notification_id,
            NotificationUser.user_id == user_id,
            NotificationUser.deleted_at.is_(None),
        )
    )

    if relation is None:
        raise NotificationError(
            "Notification not found."
        )

    if relation.read_at is None:

        relation.read_at = datetime.now(
            timezone.utc,
        )

        relation.status = "READ"

        db.commit()
        db.refresh(relation)

    return relation


def reply_notification(
    db: Session,
    notification_id: uuid.UUID,
    user_id: uuid.UUID,
    data: NotificationReply,
) -> NotificationUser:

    relation = db.scalar(
        select(NotificationUser).where(
            NotificationUser.notification_id == notification_id,
            NotificationUser.user_id == user_id,
            NotificationUser.deleted_at.is_(None),
        )
    )

    if relation is None:
        raise NotificationError(
            "Notification not found."
        )

    relation.reply = data.reply
    relation.reply_at = datetime.now(
        timezone.utc,
    )

    relation.status = "REPLIED"

    if relation.read_at is None:
        relation.read_at = relation.reply_at

    db.commit()
    db.refresh(relation)

    return relation


def unread_count(
    db: Session,
    user_id: uuid.UUID,
) -> int:

    return (
        db.scalar(
            select(
                func.count()
            )
            .select_from(NotificationUser)
            .where(
                NotificationUser.user_id == user_id,
                NotificationUser.read_at.is_(None),
                NotificationUser.deleted_at.is_(None),
            )
        )
        or 0
    )


def update_notification(
    db: Session,
    notification: Notification,
    data: NotificationUpdate,
) -> Notification:

    values = data.model_dump(
        exclude_unset=True,
    )

    for key, value in values.items():
        setattr(notification, key, value)

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(
    db: Session,
    notification: Notification,
    deleted_by: uuid.UUID,
) -> None:

    notification.deleted_at = datetime.now(
        timezone.utc,
    )

    notification.deleted_by = deleted_by
    notification.is_active = False

    db.commit()