from sqlalchemy.orm import Session
from database.connection import engine, Base
from models.models import User, Role, Permission
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt


def seed_data():
    # create tables
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    try:
        # ---- Permissions ----
        permissions_data = [
            {"name": "View Users", "description": "Can view users", "resource": "users", "action": "read"},
            {"name": "Create User", "description": "Can create users", "resource": "users", "action": "create"},
            {"name": "Edit User", "description": "Can edit users", "resource": "users", "action": "update"},
            {"name": "Delete User", "description": "Can delete users", "resource": "users", "action": "delete"},
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
            admin_role = Role(name="admin", description="Administrator with full access")
            session.add(admin_role)

        user_role = session.query(Role).filter_by(name="user").first()
        if not user_role:
            user_role = Role(name="user", description="Regular user with limited access")
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
    seed_data()
