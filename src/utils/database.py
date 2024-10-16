from contextlib import contextmanager
from src import SessionLocal
import logging

# Dependency function to get a new database session
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        try:
            session.close()
        except Exception as e:
            logging.error(f"Error closing session: {e}")