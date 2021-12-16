#from sqlalchemy.orm import Session
from db.db_init import SessionLocal

def get_db():
    #session = Session()
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
