"""
Reset and initialize database
Drops all existing tables and recreates them from scratch
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

def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Dropping existing tables...")

        # Drop tables in reverse order of dependencies
        drop_statements = [
            "DROP TABLE IF EXISTS login_history",
            "DROP TABLE IF EXISTS order_detail",
            "DROP TABLE IF EXISTS `order`",
            "DROP TABLE IF EXISTS pizza",
            "DROP TABLE IF EXISTS customer",
            "DROP TABLE IF EXISTS employee"
        ]

        for statement in drop_statements:
            cursor.execute(statement)

        conn.commit()
        print("Old tables dropped successfully!")

        print("Creating new tables...")

        # Create tables
        cursor.execute("""
            CREATE TABLE customer (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE pizza (
                pizza_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                size VARCHAR(20) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                cost DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE employee (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE `order` (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE order_detail (
                order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                pizza_id INT NOT NULL,
                quantity INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES `order`(order_id),
                FOREIGN KEY (pizza_id) REFERENCES pizza(pizza_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE login_history (
                login_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                user_agent VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES employee(user_id)
            )
        """)

        conn.commit()
        print("Tables created successfully!")

        print("Inserting sample data...")

        # Insert customers
        cursor.execute("""
            INSERT INTO customer (name, phone, email) VALUES
            ('John Smith', '555-0101', 'john.smith@email.com'),
            ('Jane Doe', '555-0102', 'jane.doe@email.com'),
            ('Michael Johnson', '555-0103', 'michael.j@email.com'),
            ('Sarah Williams', '555-0104', 'sarah.w@email.com'),
            ('David Brown', '555-0105', 'david.brown@email.com')
        """)

        # Insert pizzas
        cursor.execute("""
            INSERT INTO pizza (name, size, price, cost) VALUES
            ('Margherita', 'Small', 8.99, 3.50),
            ('Margherita', 'Medium', 12.99, 5.00),
            ('Margherita', 'Large', 16.99, 6.50),
            ('Pepperoni', 'Small', 9.99, 4.00),
            ('Pepperoni', 'Medium', 13.99, 5.50),
            ('Pepperoni', 'Large', 17.99, 7.00),
            ('Vegetarian', 'Small', 10.99, 4.50),
            ('Vegetarian', 'Medium', 14.99, 6.00),
            ('Vegetarian', 'Large', 18.99, 7.50),
            ('Hawaiian', 'Small', 10.99, 4.50),
            ('Hawaiian', 'Medium', 14.99, 6.00),
            ('Hawaiian', 'Large', 18.99, 7.50),
            ('Meat Lovers', 'Small', 12.99, 5.50),
            ('Meat Lovers', 'Medium', 16.99, 7.00),
            ('Meat Lovers', 'Large', 20.99, 8.50)
        """)

        # Insert employees
        cursor.execute("""
            INSERT INTO employee (username, first_name, last_name, password) VALUES
            ('admin', 'Admin', 'User', 'admin123'),
            ('jsmith', 'John', 'Smith', 'password123'),
            ('mdavis', 'Mary', 'Davis', 'password123'),
            ('rjones', 'Robert', 'Jones', 'password123')
        """)

        # Insert orders
        cursor.execute("""
            INSERT INTO `order` (customer_id, date) VALUES
            (1, '2025-10-20'),
            (2, '2025-10-20'),
            (3, '2025-10-21'),
            (1, '2025-10-21'),
            (4, '2025-10-22')
        """)

        # Insert order details
        cursor.execute("""
            INSERT INTO order_detail (order_id, pizza_id, quantity) VALUES
            (1, 2, 1),
            (1, 5, 1),
            (2, 6, 2),
            (3, 8, 1),
            (3, 11, 1),
            (4, 15, 1),
            (5, 1, 3),
            (5, 4, 2)
        """)

        conn.commit()
        print("Sample data inserted successfully!")
        print("\nDatabase reset complete!")
        print("\nDefault login credentials:")
        print("  Username: admin")
        print("  Password: admin123")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    reset_database()
