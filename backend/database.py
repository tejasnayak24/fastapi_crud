from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect, text


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = "postgresql://postgres.dvxlryatqcrsaaqrfkec:feX1YXUZMs80E0MF@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_schema():
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    missing_columns = {
        "hashed_password": "ALTER TABLE users ADD COLUMN hashed_password VARCHAR",
    }

    with engine.begin() as connection:
        for column_name, statement in missing_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(statement))
