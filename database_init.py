from main import create_app
from app.models.models import db, User, ActivityLog, File, Alert
from app.detection_engine.engine import train_model
from flask_bcrypt import Bcrypt
import random
import os
from datetime import datetime, timedelta

bcrypt = Bcrypt()

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Initializing database...")
        
        # 1. Create Users
        users_data = [
            ('admin', 'admin@itd.com', 'admin123', 'Admin', 'Cybersecurity'),
            ('manager_sarah', 'sarah@itd.com', 'manager123', 'Manager', 'Engineering'),
            ('emp_john', 'john@itd.com', 'user123', 'Employee', 'Engineering'),
            ('emp_alice', 'alice@itd.com', 'user123', 'Employee', 'Finance'),
            ('emp_bob', 'bob@itd.com', 'user123', 'Employee', 'IT Operations'),
        ]
        
        users = []
        for uname, email, pwd, role, dept in users_data:
            hashed = bcrypt.generate_password_hash(pwd).decode('utf-8')
            user = User(username=uname, email=email, password_hash=hashed, role=role, department=dept)
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Created {len(users)} users.")

        # 2. Create Sample Files
        # Ensure upload folder exists with absolute path
        basedir = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basedir, 'database', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        files_data = [
            ('q1_financial_report.pdf', True),
            ('employee_salary_list.xlsx', True),
            ('network_architecture_v2.png', False),
            ('product_roadmap_2026.docx', False),
            ('it_security_policy.pdf', False),
        ]
        
        for fname, confidential in files_data:
            file_full_path = os.path.join(upload_dir, fname)
            # Create dummy file if not exists
            if not os.path.exists(file_full_path):
                with open(file_full_path, 'w') as f:
                    f.write(f"Sample content for {fname}")
            
            file = File(
                filename=fname,
                file_path=file_full_path,
                is_confidential=confidential,
                uploaded_by=users[0].id
            )
            db.session.add(file)
        
        db.session.commit()
        print(f"Created {len(files_data)} sample files.")

        # 3. Create Normal Activity History
        print("Generating normal activity history...")
        for user in users:
            # Each user has 20-30 normal activities during work hours
            for _ in range(random.randint(20, 30)):
                # Normal work hours: 9 AM - 6 PM
                hour = random.randint(9, 17)
                minute = random.randint(0, 59)
                days_ago = random.randint(1, 10)
                ts = datetime.utcnow() - timedelta(days=days_ago)
                ts = ts.replace(hour=hour, minute=minute)
                
                action = random.choice(['login', 'page_view', 'page_view', 'logout'])
                log = ActivityLog(
                    user_id=user.id,
                    action_type=action,
                    details='{"status": "success", "ip": "192.168.1.10"}',
                    timestamp=ts,
                    is_anomaly=False
                )
                db.session.add(log)
        
        db.session.commit()

        # 4. Create Anomaly Activities (The "Insider Threat" simulation)
        print("Simulating insider threat anomalies...")
        # Alice (Finance) accessing files at 2 AM
        alice = User.query.filter_by(username='emp_alice').first()
        ts_anomaly = datetime.utcnow() - timedelta(hours=22) # Late night
        ts_anomaly = ts_anomaly.replace(hour=2, minute=15)
        
        anomaly_log = ActivityLog(
            user_id=alice.id,
            action_type='file_access',
            details='{"filename": "employee_salary_list.xlsx", "action": "download"}',
            timestamp=ts_anomaly,
            is_anomaly=True,
            anomaly_score=0.85
        )
        db.session.add(anomaly_log)
        
        # Create alert for this anomaly
        alert = Alert(
            user_id=alice.id,
            severity='High',
            description="Late night sensitive file access detected",
            timestamp=ts_anomaly,
            model_explanation="Access to confidential finance data outside of established 9-5 work hours (2:15 AM). Alice typically works during standard hours.",
            status='Open'
        )
        db.session.add(alert)
        alice.risk_score = 85.0
        
        # Bob (IT) multiple failed login attempts
        bob = User.query.filter_by(username='emp_bob').first()
        ts_bob = datetime.utcnow() - timedelta(hours=5)
        for _ in range(4):
            failed_log = ActivityLog(
                user_id=bob.id,
                action_type='failed_login',
                details='{"ip": "10.0.0.45", "attempt": "failed"}',
                timestamp=ts_bob,
                is_anomaly=True,
                anomaly_score=0.65
            )
            db.session.add(failed_log)
        
        alert_bob = Alert(
            user_id=bob.id,
            severity='Medium',
            description="Brute force login attempt detected",
            timestamp=ts_bob,
            model_explanation="4 consecutive failed login attempts detected within 2 minutes from internal IP 10.0.0.45.",
            status='Open'
        )
        db.session.add(alert_bob)
        bob.risk_score = 45.0
        
        db.session.commit()
        print("Seeding complete.")

        # 5. Train Model
        print("Training AI Detection Engine...")
        train_model()
        print("Model trained and saved.")

if __name__ == '__main__':
    seed_database()
