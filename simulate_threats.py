from main import create_app
from app.models.models import db, User, ActivityLog, Alert
from app.detection_engine.engine import check_activity_for_anomaly
from datetime import datetime
import json
import time

from run_dev import DevConfig
app = create_app(config_object=DevConfig)

with app.app_context():
    # Ensure Super Admin and Employee exist
    super_admin = User.query.filter_by(role='Super Admin').first()
    if not super_admin:
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash('super123').decode('utf-8')
        super_admin = User(username='superadmin', email='super@itd-system.com', password_hash=hashed_password, role='Super Admin', department='Cybersecurity')
        db.session.add(super_admin)
    
    employee = User.query.filter_by(username='bad_employee').first()
    if not employee:
        employee = User(username='bad_employee', email='bad@itd-system.com', password_hash='pw', role='Employee', department='Engineering')
        db.session.add(employee)
    db.session.commit()

    print("Simulating Logic Bomb precursor sequence for 'bad_employee'...")
    
    # 1. cron_mod
    log1 = ActivityLog(user_id=employee.id, action_type='cron_mod', details=json.dumps({'cmd': 'crontab -e'}), source_ip='192.168.1.55')
    db.session.add(log1)
    db.session.commit()
    check_activity_for_anomaly(log1)
    
    # 2. file_access
    log2 = ActivityLog(user_id=employee.id, action_type='file_access', details=json.dumps({'file': '/etc/passwd'}), source_ip='192.168.1.55')
    db.session.add(log2)
    db.session.commit()
    check_activity_for_anomaly(log2)
    
    # 3. sudo_escalation (Triggers Logic Bomb LSTM simulation)
    log3 = ActivityLog(user_id=employee.id, action_type='sudo_escalation', details=json.dumps({'cmd': 'sudo su -'}), source_ip='192.168.1.55')
    db.session.add(log3)
    db.session.commit()
    check_activity_for_anomaly(log3)
    
    print("Threat simulation completed. Check ForensicReport table.")
