"""
Database initialization script - Fixed version
Creates tables first, then inserts data
"""
import pymysql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    """Get database connection from environment variables"""
    # Check for Heroku database URLs (JawsDB or ClearDB)
    jawsdb_url = os.getenv('JAWSDB_URL')
    cleardb_url = os.getenv('CLEARDB_DATABASE_URL')
    heroku_db_url = jawsdb_url or cleardb_url

    if heroku_db_url:
        # Parse Heroku database URL
        url = urlparse(heroku_db_url)
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

        # Read schema.sql
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Execute schema creation
        statements = [s.strip() for s in schema_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        for statement in statements:
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("Tables created successfully!")

        print("Inserting sample data...")

        # Read seed_data.sql
        with open('database/seed_data.sql', 'r', encoding='utf-8') as f:
            seed_sql = f.read()

        # Execute seed data insertion
        statements = [s.strip() for s in seed_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        for statement in statements:
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("Sample data inserted successfully!")
        print("\nDatabase initialization complete!")
        print("\nDefault login credentials:")
        print("  Username: admin")
        print("  Password: admin123")

    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_database()
