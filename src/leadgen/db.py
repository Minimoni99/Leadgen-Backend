import os
from pathlib import Path
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_DSN = (
    f"dbname={os.getenv('POSTGRES_DB', 'leadgen')} "
    f"user={os.getenv('POSTGRES_USER', 'leadgen')} "
    f"password={os.getenv('POSTGRES_PASSWORD', 'leadgen')} "
    f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
    f"port={os.getenv('POSTGRES_PORT', '5432')}"
)


def connect():
    return psycopg.connect(DB_DSN, row_factory=dict_row)


def init_db(schema_path: Optional[Path] = None):
    schema_path = schema_path or BASE_DIR / "db" / "schema.sql"
    with connect() as conn:
        with conn.cursor() as cur:
            with open(schema_path, "r", encoding="utf-8") as schema_file:
                cur.execute(schema_file.read())
        conn.commit()
    print(f"Initialized database schema from {schema_path}")
