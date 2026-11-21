import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.db import get_db, SessionLocal

def test_get_db_yields_valid_session():
    """Verify that get_db() yields a valid SQLAlchemy Session instance."""
    gen = get_db()
    session = next(gen)
    try:
        assert isinstance(session, Session)
        assert session.bind is not None
    finally:
        try:
            next(gen)
        except StopIteration:
            pass

def test_get_db_session_is_closed_after_cleanup():
    """Verify that the yielded session is closed when generator cleans up."""
    gen = get_db()
    session = next(gen)
    
    # Spy on session.close
    original_close = session.close
    close_called = []
    
    def spy_close():
        close_called.append(True)
        original_close()
        
    session.close = spy_close
    
    # Trigger generator teardown (finally block)
    try:
        next(gen)
    except StopIteration:
        pass
        
    assert len(close_called) == 1, "session.close() was not called in finally block"

def test_get_db_yields_distinct_sessions():
    """Verify that two sequential/concurrent invocations receive distinct Session instances."""
    gen1 = get_db()
    gen2 = get_db()
    
    session1 = next(gen1)
    session2 = next(gen2)
    
    try:
        assert session1 is not session2, "get_db() must yield isolated sessions, not a shared instance"
    finally:
        try:
            next(gen1)
        except StopIteration:
            pass
        try:
            next(gen2)
        except StopIteration:
            pass
