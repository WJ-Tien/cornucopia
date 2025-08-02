from .base_init import Base
from .config import CORNU_DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.db_session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        """
        Dependency to get a database session.
        """
        db = self.db_session()
        try:
            yield db
        finally:
            db.close()

    def create_all_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def drop_all_tables(self):
        Base.metadata.drop_all(bind=self.engine)

db_manager = DatabaseManager(CORNU_DB_URL)