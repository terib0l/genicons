from app.db.db_init import SessionLocal


def get_db():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()
