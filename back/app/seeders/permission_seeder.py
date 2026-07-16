from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


def run(db: Session) -> None:

    permissions = [
        # People
        ("people.create", "Create people"),
        ("people.read", "Read people"),
        ("people.update", "Update people"),
        ("people.delete", "Delete people"),

        # Users
        ("users.create", "Create Users"),
        ("users.update", "Update Users"),
        ("users.delete", "Delete Users"),
        ("users.read", "Read users"),
        ("users.unlock", "Unlock users"),
        ("users.reset_password", "Reset Password"),

        # Roles
        ("roles.create", "Create Roles"),
        ("roles.update", "Update Roles"),
        ("roles.delete", "Delete Roles"),
        ("roles.read", "Read Roles"),

        # Permissions
        ("permissions.create", "Create permissions"),
        ("permissions.read", "Read permissions"),
        ("permissions.update", "Update permissions"),
        ("permissions.delete", "Delete permissions"),

        # Files
        ("files.read", "Read Files"),
        ("files.create", "Create Files"),
        ("files.update", "Update Files"),
        ("files.delete", "Delete Files"),

        # Audit
        ("audit.read", "Read Audit"),

        # Profile
        ("profile.read", "Read Profile"),
        ("profile.update", "Update Profile"),
        ("profile.change_password", "Change Password"),

        # Notifications
        ("notifications.read","Read Notifications"),
        ("notifications.create","Create Notifications"),
        ("notifications.update","Update Notifications"),
        ("notifications.delete","Delete Notifications"),
        ("notifications.reply","Reply Notifications"),

        # Organization
        ("organization.read", "Read Organization"),
        ("organization.update", "Update Organization"),

        # Themes
        ("themes.read", "Read Themes"),
        ("themes.update", "Update Themes"),
    ]

    for code, name in permissions:

        exists = db.scalar(
            select(Permission).where(
                Permission.code == code
            )
        )

        if exists:
            continue

        db.add(
            Permission(
                code=code,
                name=name,
            )
        )

    db.commit()