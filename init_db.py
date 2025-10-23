"""
Database initialization script for Heroku ClearDB
This script creates all tables and populates them with sample data
"""
import pymysql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    """Get database connection from environment variables"""
    cleardb_url = os.getenv('CLEARDB_DATABASE_URL')

    if cleardb_url:
        # Parse ClearDB URL for Heroku
        url = urlparse(cleardb_url)
        return pymysql.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            port=url.port or 3306
        )
    else:
        # Use individual environment variables for local
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306))
        )

def init_database():
    """Initialize database with schema and seed data"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Creating database tables...")

        # Read and execute schema.sql
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()

        # Execute each statement separately
        for statement in schema_sql.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)

        print("✓ Tables created successfully")

        print("Inserting sample data...")

        # Read and execute seed_data.sql
        with open('database/seed_data.sql', 'r') as f:
            seed_sql = f.read()

        # Execute each statement separately
        for statement in seed_sql.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)

        conn.commit()
        print("✓ Sample data inserted successfully")
        print("\n✓ Database initialization complete!")
        print("\nDefault login credentials:")
        print("  Username: admin")
        print("  Password: admin123")

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_database()
