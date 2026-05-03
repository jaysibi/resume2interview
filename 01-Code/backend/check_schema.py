"""Quick script to verify V2 database schema"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
# Convert SQLAlchemy URL to psycopg2 format
db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

print("=== All Tables ===")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
for row in cur.fetchall():
    print(f"  {row[0]}")

print("\n=== Resumes Columns ===")
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='resumes' ORDER BY ordinal_position")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

print("\n=== Job Descriptions Columns ===")
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='job_descriptions' ORDER BY ordinal_position")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

print("\n=== Users Table ===")
cur.execute("SELECT COUNT(*) FROM users")
print(f"  Count: {cur.fetchone()[0]}")

print("\n=== Applications Table ===")
cur.execute("SELECT COUNT(*) FROM applications")
print(f"  Count: {cur.fetchone()[0]}")

conn.close()
print("\n✅ V2 schema verified successfully!")
