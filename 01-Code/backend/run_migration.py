"""
Database migration runner
Executes SQL migration files in order
"""
import psycopg2
import os
import sys

def run_migration(migration_file_path):
    """Execute a SQL migration file"""
    # Database connection parameters
    db_params = {
        'dbname': 'resumetailor',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    
    try:
        # Read migration file
        with open(migration_file_path, 'r') as f:
            migration_sql = f.read()
        
        # Connect to database
        print(f"Connecting to database: {db_params['dbname']}...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Execute migration
        print(f"Executing migration: {migration_file_path}...")
        cursor.execute(migration_sql)
        
        print("✅ Migration completed successfully!")
        
        # Close connection
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Migration file not found: {migration_file_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Get migration file from command line or use default
    if len(sys.argv) > 1:
        migration_file = sys.argv[1]
    else:
        migration_file = "migrations/001_add_updated_at_column.sql"
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    migration_path = os.path.join(script_dir, migration_file)
    
    print(f"Running migration: {migration_path}")
    success = run_migration(migration_path)
    
    sys.exit(0 if success else 1)
