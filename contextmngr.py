# Use the context manage of this to perform raw queries
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Database configuration
DATABASE_URL = "sqlite:///./sms_reminder.sqlite"
DATABASE_ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Construct a session maker
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=DATABASE_ENGINE)

# Construct a scoped session
SessionLocal = scoped_session(session_factory)

# Construct a base class for declarative class definitions
Base = declarative_base()

#! can either place @contextmanager to avoid enter and exit
class DBSessionManager:
    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.session.rollback()
        except Exception:
            pass
        finally:
            self.session.close()
            SessionLocal.remove()

# Example of using the context manager to perform raw SQL queries
def perform_raw_query(query):
    with DBSessionManager() as session:
        result = session.execute(text(query))
        return result.fetchall()

# Example usage
if __name__ == "__main__":
    # Example raw query
    query = "SELECT * FROM some_table"
    results = perform_raw_query(query)
    for row in results:
        print(row)
