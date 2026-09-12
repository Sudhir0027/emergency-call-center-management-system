from datetime import datetime, timedelta, timezone
from .database import SessionLocal
from .models import User, Responder, EmergencyCall, CallHistory
from .utils.security import hash_password

def seed_database():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add_all([
                User(username="admin", email="admin@example.com", password_hash=hash_password("Admin@123"), role="ADMIN"),
                User(username="operator", email="operator@example.com", password_hash=hash_password("Operator@123"), role="OPERATOR"),
            ])
        if db.query(Responder).count() == 0:
            data = [
                ("Arun","AMBULANCE","9000000001","AMB-01","Erode","AVAILABLE"),
                ("Kumar","AMBULANCE","9000000002","AMB-02","Salem","AVAILABLE"),
                ("Priya","AMBULANCE","9000000003","AMB-03","Tiruppur","BUSY"),
                ("Ravi","POLICE","9000000004","POL-01","Erode","AVAILABLE"),
                ("Mani","POLICE","9000000005","POL-02","Salem","AVAILABLE"),
                ("Divya","POLICE","9000000006","POL-03","Coimbatore","OFFLINE"),
                ("Suresh","FIRE","9000000007","FIR-01","Erode","AVAILABLE"),
                ("Vijay","FIRE","9000000008","FIR-02","Tiruppur","BUSY"),
                ("Mohan","RESCUE","9000000009","RES-01","Salem","AVAILABLE"),
                ("Anitha","RESCUE","9000000010","RES-02","Coimbatore","AVAILABLE"),
            ]
            db.add_all([Responder(name=n,type=t,phone=p,vehicle_number=v,location=l,availability=a) for n,t,p,v,l,a in data])
            db.flush()
        if db.query(EmergencyCall).count() == 0:
            now = datetime.now(timezone.utc)
            calls = [
                (101,"Karthik","9876500001","Erode","Road Accident","Two vehicles collided near the main road.",3,"WAITING"),
                (102,"Meena","9876500002","Salem","Medical Emergency","Severe breathing difficulty reported.",5,"WAITING"),
                (103,"Ramesh","9876500003","Tiruppur","Fire","Building fire reported by caller.",5,"WAITING"),
                (104,"Lakshmi","9876500004","Coimbatore","Missing Person","Child reported missing.",2,"WAITING"),
                (105,"Arun","9876500005","Chennai","Police","Break-in reported at a residence.",4,"WAITING"),
                (106,"Sathya","9876500006","Erode","Rescue","Person trapped after a minor collapse.",4,"ASSIGNED"),
                (107,"Naveen","9876500007","Salem","Medical Emergency","Patient needs urgent transport.",5,"IN_PROGRESS"),
                (108,"Geetha","9876500008","Tiruppur","Fire","Smoke detected in a warehouse.",3,"RESOLVED"),
                (109,"Bala","9876500009","Erode","Police","Traffic incident requiring assistance.",2,"CANCELLED"),
                (110,"Divya","9876500010","Coimbatore","Natural Disaster","Local flooding reported.",3,"WAITING"),
            ]
            for cid,name,phone,loc,typ,desc,priority,status in calls:
                c = EmergencyCall(call_id=cid, caller_name=name, caller_phone=phone, location=loc,
                                  emergency_type=typ, description=desc, priority=priority, status=status,
                                  created_at=now-timedelta(minutes=cid-100))
                if status == "ASSIGNED": c.assigned_responder_id = 9
                if status == "IN_PROGRESS": c.assigned_responder_id = 3
                db.add(c)
                db.flush()
                db.add(CallHistory(call_id=cid, old_status=None, new_status="WAITING", changed_by="system"))
                if status != "WAITING":
                    db.add(CallHistory(call_id=cid, old_status="WAITING", new_status=status, changed_by="system"))
        db.commit()
    finally:
        db.close()
