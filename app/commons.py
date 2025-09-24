"""Commons methods."""

from app.database import session


def get_db():
    """Get database session."""
    db = session()
    try:
        yield db
    finally:
        db.close()
