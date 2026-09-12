from app.database import Base, engine, SessionLocal
from app.models import EmergencyCall
from app.services.priority_queue import get_priority_queue

def test_priority_order():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        db.query(EmergencyCall).delete()
        db.add_all([
            EmergencyCall(call_id=101,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=3,status="WAITING"),
            EmergencyCall(call_id=102,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=5,status="WAITING"),
            EmergencyCall(call_id=103,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=5,status="WAITING"),
            EmergencyCall(call_id=104,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=2,status="WAITING"),
            EmergencyCall(call_id=105,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=4,status="WAITING"),
            EmergencyCall(call_id=106,caller_name="a",caller_phone="1",location="x",emergency_type="Other",description="x",priority=5,status="RESOLVED"),
        ])
        db.commit()
        assert [c.call_id for c in get_priority_queue(db)] == [102,103,105,101,104]
    finally:
        db.close()
