from app.database.db import SessionLocal
from app.models.log import Log
from app.models.user import User
from app.tests.fixtures.load_sample_logs import load_sample_logs

TEST_EMAIL = "test@example.com"

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