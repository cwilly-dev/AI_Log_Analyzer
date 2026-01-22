from app.database.db import SessionLocal
from app.models import User
from app.core.security import hash_password

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"

def seed_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == TEST_EMAIL).first()
        if user:
            print("Test user already exists")
            return user

        user = User(
            email=TEST_EMAIL,
            hashed_password=hash_password(TEST_PASSWORD),
        )
        db.add(user)
        db.commit()
        db.refresh(user)


        print(f"Created test user (id={user.id})")
        return user
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()