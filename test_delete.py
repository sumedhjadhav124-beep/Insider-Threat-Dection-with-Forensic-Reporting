from main import app
from app.models.models import db, User, ActivityLog
import sys

def test_delete():
    with app.app_context():
        # Find a user who has activity logs
        user = User.query.join(ActivityLog).first()
        if not user:
            print("No user with activity logs found to test.")
            return
        
        print(f"Attempting to delete user: {user.username} (ID: {user.id})")
        try:
            db.session.delete(user)
            db.session.commit()
            print("Deletion successful (Wait, it should have failed if constraints are working!)")
        except Exception as e:
            db.session.rollback()
            print(f"Deletion failed as expected: {type(e).__name__}")
            print(str(e))

if __name__ == "__main__":
    test_delete()
