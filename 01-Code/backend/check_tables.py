from db import engine
from sqlalchemy import text, inspect

# Check using inspector
inspector = inspect(engine)
tables = inspector.get_table_names()

print("\n=== TABLES (Inspector) ===")
for table in sorted(tables):
    print(f"  ✓ {table}")
print(f"\nTotal: {len(tables)}")

# Check using SQL query
print("\n=== TABLES (pg_tables) ===")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema') 
        ORDER BY tablename
    """))
    tables_sql = result.fetchall()
    for schema, table in tables_sql:
        print(f"  {schema}.{table}")
    print(f"\nTotal: {len(tables_sql)}")

# Check alembic_version
print("\n=== ALEMBIC VERSION ===")
with engine.connect() as conn:
    try:
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        version = result.fetchone()
        if version:
            print(f"  Current: {version[0]}")
        else:
            print("  No version found")
    except Exception as e:
        print(f"  Error: {e}")
