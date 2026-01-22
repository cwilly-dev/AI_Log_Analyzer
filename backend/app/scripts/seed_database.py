
from app.core.security import hash_password
from app.database.db import SessionLocal
from app.models.log import Log
from app.models.user import User
from app.scripts.fixtures.load_sample_logs import load_sample_logs

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

def seed_logs():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == TEST_EMAIL).first()
        if not user:
            raise RuntimeError("Test user not found. Please run seed_test_user first.")

        logs = load_sample_logs()
        for item in logs:
            log = Log(
                owner_id=user.id,
                content=item["content"],
            )
            db.add(log)

        db.commit()
        print(f"Seeded {len(logs)} logs for user {user.email}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_logs()