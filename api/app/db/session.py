from sqlalchemy.orm import Session

def get_db():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
