"""
Migration: add public_id UUID column to resumes and job_descriptions tables.
Safe to run multiple times (checks if column exists first).
"""
import uuid
from db import engine
from sqlalchemy import text

def column_exists(conn, table: str, column: str) -> bool:
    result = conn.execute(text(
        "SELECT 1 FROM information_schema.columns "
        "WHERE table_name = :t AND column_name = :c"
    ), {"t": table, "c": column})
    return result.fetchone() is not None

def run():
    with engine.begin() as conn:
        for table in ("resumes", "job_descriptions"):
            if column_exists(conn, table, "public_id"):
                print(f"  {table}.public_id already exists — skipping.")
                continue

            # Add nullable column first, then backfill, then add constraints
            print(f"  Adding public_id to {table}...")
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN public_id VARCHAR(36)"))

            # Backfill UUIDs for existing rows
            rows = conn.execute(text(f"SELECT id FROM {table}")).fetchall()
            for (row_id,) in rows:
                conn.execute(
                    text(f"UPDATE {table} SET public_id = :uid WHERE id = :id"),
                    {"uid": str(uuid.uuid4()), "id": row_id}
                )
            print(f"  Backfilled {len(rows)} rows in {table}.")

            # Add NOT NULL + UNIQUE constraints
            conn.execute(text(f"ALTER TABLE {table} ALTER COLUMN public_id SET NOT NULL"))
            conn.execute(text(f"ALTER TABLE {table} ADD CONSTRAINT uq_{table}_public_id UNIQUE (public_id)"))
            conn.execute(text(f"CREATE INDEX ix_{table}_public_id ON {table} (public_id)"))
            print(f"  Constraints and index added to {table}.")

    print("Migration complete.")

if __name__ == "__main__":
    run()
