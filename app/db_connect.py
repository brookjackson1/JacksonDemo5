import pymysql
import pymysql.cursors
from flask import g
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        try:
            # Check if CLEARDB_DATABASE_URL exists (Heroku ClearDB)
            cleardb_url = os.getenv('CLEARDB_DATABASE_URL')

            if cleardb_url:
                # Parse ClearDB URL: mysql://user:password@host/database
                url = urlparse(cleardb_url)
                g.db = pymysql.connect(
                    host=url.hostname,
                    user=url.username,
                    password=url.password,
                    database=url.path[1:],  # Remove leading slash
                    port=url.port or 3306,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Connected to Heroku ClearDB")
            else:
                # Use individual environment variables (local development)
                g.db = pymysql.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME'),
                    port=int(os.getenv('DB_PORT', 3306)),
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Connected to local/AWS RDS database")
        except Exception as e:
            print(f"Database connection failed: {e}")
            g.db = None
            return None
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()