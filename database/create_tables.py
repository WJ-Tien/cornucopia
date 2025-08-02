from backend.app.core.database import db_manager 
from backend.app.models import user # noqa

if __name__ == "__main__":

    db_manager.create_all_tables()
    print("Database tables created successfully.")