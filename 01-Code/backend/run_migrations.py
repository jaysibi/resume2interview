#!/usr/bin/env python
"""Simple script to run Alembic migrations"""
import subprocess
import sys

print("Running database migrations...")
try:
    result = subprocess.run(
        ["python", "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    print("✅ Migrations completed successfully!")
    sys.exit(0)
except subprocess.CalledProcessError as e:
    print(f"❌ Migration failed:")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)
