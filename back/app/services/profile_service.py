from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.profile import (
    ChangePasswordRequest,
    ProfileUpdate,
)


class ProfileError(Exception):
    pass


def update_profile(
    db: Session,
    user: User,
    data: ProfileUpdate,
) -> User:

    values = data.model_dump(
        exclude_unset=True,
    )

    person = user.person

    for key, value in values.items():
        setattr(person, key, value)

    db.commit()
    db.refresh(user)

    return user


def change_password(
    db: Session,
    user: User,
    data: ChangePasswordRequest,
) -> User:

    if not verify_password(
        data.current_password,
        user.hashed_password,
    ):
        raise ProfileError(
            "Current password is incorrect."
        )

    user.hashed_password = hash_password(
        data.new_password
    )

    user.failed_login_attempts = 0
    user.is_locked = False

    db.commit()
    db.refresh(user)

    return user