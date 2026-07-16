from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.seeders.gender_seeder import run as gender_seeder
from app.seeders.document_type_seeder import run as document_type_seeder
from app.seeders.role_seeder import run as role_seeder
from app.seeders.permission_seeder import run as permission_seeder
from app.seeders.admin_seeder import run as admin_seeder
from app.seeders.role_permission_seeder import run as role_permission_seeder
from app.seeders.theme_seeder import run as theme_seeder
from app.seeders.organization_setting_seeder import run as organization_setting_seeder


def run() -> None:

    db: Session = SessionLocal()

    try:

        print("Seeding genders...")
        gender_seeder(db)

        print("Seeding document types...")
        document_type_seeder(db)

        print("Seeding roles...")
        role_seeder(db)

        print("Seeding permissions...")
        permission_seeder(db)

        print("Seeding administrator...")
        admin_seeder(db)

        print("Seeding role permissions...")
        role_permission_seeder(db)

        print("Seeding theme...")
        theme_seeder(db)

        print("Seeding organization settings...")
        organization_setting_seeder(db)

        print("Seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run()