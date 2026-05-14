import os
import psycopg2

# Connect to database
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Get all tables
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' 
    ORDER BY table_name;
""")

tables = cur.fetchall()

print(f"\n✅ Tables in database ({len(tables)} total):")
for table in tables:
    print(f"  - {table[0]}")

# Check if alembic_version exists and get version
try:
    cur.execute("SELECT version_num FROM alembic_version")
    version = cur.fetchone()
    if version:
        print(f"\n✅ Alembic version: {version[0]}")
except:
    print("\n❌ No alembic_version table found")

cur.close()
conn.close()
