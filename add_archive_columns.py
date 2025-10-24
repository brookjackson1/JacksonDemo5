"""
Add archive columns to customer and pizza tables
This preserves data integrity by archiving instead of deleting
"""
import pymysql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    """Get database connection from environment variables"""
    jawsdb_url = os.getenv('JAWSDB_URL')
    cleardb_url = os.getenv('CLEARDB_DATABASE_URL')
    heroku_db_url = jawsdb_url or cleardb_url

    if heroku_db_url:
        url = urlparse(heroku_db_url)
        return pymysql.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            port=url.port or 3306
        )
    else:
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306))
        )

def add_archive_columns():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Adding archive columns to customer table...")
        try:
            cursor.execute("""
                ALTER TABLE customer
                ADD COLUMN is_archived BOOLEAN DEFAULT FALSE,
                ADD COLUMN archived_at TIMESTAMP NULL
            """)
            conn.commit()
            print("Customer archive columns added successfully!")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("Customer archive columns already exist - skipping")
            else:
                raise

        print("Adding archive columns to pizza table...")
        try:
            cursor.execute("""
                ALTER TABLE pizza
                ADD COLUMN is_archived BOOLEAN DEFAULT FALSE,
                ADD COLUMN archived_at TIMESTAMP NULL
            """)
            conn.commit()
            print("Pizza archive columns added successfully!")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("Pizza archive columns already exist - skipping")
            else:
                raise

        print("\nArchive functionality ready!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_archive_columns()
