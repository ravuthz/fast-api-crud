from sqlalchemy.orm import Session
from database.connection import engine, Base
from models.models import User, Role, Permission
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt


def make_crud(resource):
    return [
        {
            "name": f"View {resource}",
            "description": f"Can view {resource}",
            "resource": resource,
            "action": "read",
        },
        {
            "name": f"Create {resource}",
            "description": f"Can create {resource}",
            "resource": resource,
            "action": "create",
        },
        {
            "name": f"Edit {resource}",
            "description": f"Can edit {resource}",
            "resource": resource,
            "action": "update",
        },
        {
            "name": f"Delete {resource}",
            "description": f"Can delete {resource}",
            "resource": resource,
            "action": "delete",
        },
    ]


def seed_data(refresh: bool = False):
    # create tables
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    try:
        if refresh:
            print("⚠️  Refresh mode enabled: truncating all tables...")
            # Drop all rows in all tables
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()

        # ---- Permissions ----
        permissions_data = [
            *make_crud("users"),
            *make_crud("roles"),
            *make_crud("permissions"),
        ]

        permissions = []
        for pdata in permissions_data:
            perm = session.query(Permission).filter_by(name=pdata["name"]).first()
            if not perm:
                perm = Permission(**pdata)
                session.add(perm)
            permissions.append(perm)

        # ---- Roles ----
        admin_role = session.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(
                name="admin", description="Administrator with full access"
            )
            session.add(admin_role)

        user_role = session.query(Role).filter_by(name="user").first()
        if not user_role:
            user_role = Role(
                name="user", description="Regular user with limited access"
            )
            session.add(user_role)

        session.flush()  # flush to get IDs

        # assign all permissions to admin
        admin_role.permissions = permissions

        # assign only view permission to user
        user_role.permissions = [permissions[0]]

        # ---- Default Admin User ----
        admin_user = session.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=bcrypt.hash("admin123"),
                is_active=True,
                roles=[admin_role],
            )
            session.add(admin_user)

        session.commit()
        print("✅ Data seeding completed")

    except IntegrityError as e:
        session.rollback()
        print("⚠️ Seeding failed:", e)

    finally:
        session.close()


if __name__ == "__main__":
    import sys

    refresh_flag = "--refresh" in sys.argv
    seed_data(refresh=refresh_flag)
