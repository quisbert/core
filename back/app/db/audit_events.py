from sqlalchemy import event, inspect
from sqlalchemy.orm import Session


@event.listens_for(Session, "before_flush")
def apply_audit_fields(
    session: Session,
    flush_context,
    instances,
) -> None:
    user_id = session.info.get("current_user_id")

    if user_id is None:
        return

    for instance in session.new:
        if (
            hasattr(instance, "created_by")
            and instance.created_by is None
        ):
            instance.created_by = user_id

    for instance in session.dirty:
        if not session.is_modified(
            instance,
            include_collections=False,
        ):
            continue

        if hasattr(instance, "updated_by"):
            instance.updated_by = user_id

        if hasattr(instance, "deleted_at"):
            state = inspect(instance)

            if (
                "deleted_at" in state.attrs
                and state.attrs.deleted_at.history.has_changes()
                and instance.deleted_at is not None
                and hasattr(instance, "deleted_by")
            ):
                instance.deleted_by = user_id