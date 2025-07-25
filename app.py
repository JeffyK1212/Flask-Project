from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import MYSQL_CONFIG
import mysql.connector
from config import MYSQL_CONFIG
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)


def initialize_database():
    try:
        
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        
        cursor.execute("DROP TABLE IF EXISTS shipping")
        cursor.execute("DROP TABLE IF EXISTS inventory")
        cursor.execute("DROP TABLE IF EXISTS products")
        
       
        cursor.execute("""
        CREATE TABLE products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL
        ) ENGINE=InnoDB
        """)
        
        cursor.execute("""
        CREATE TABLE inventory (
            inventory_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            FOREIGN KEY (product_id) 
                REFERENCES products(product_id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB
        """)
        
        cursor.execute("""
        CREATE TABLE shipping (
            shipping_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            next_shipment_date DATE NOT NULL,
            FOREIGN KEY (product_id) 
                REFERENCES products(product_id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB
        """)
        
       
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        
        
        conn.commit()
        print("Database initialized successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    try:
       
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.close()
        
        
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
       
        cursor.execute("USE inventory_db")  
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL
        ) ENGINE=InnoDB
        """)
        
        
        
        conn.commit()
        print("Database initialized successfully!")
        try:
            
            conn = mysql.connector.connect(
                host=MYSQL_CONFIG['host'],
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password']
            )
            cursor = conn.cursor()
            
           
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
            cursor.close()
            conn.close()
            
            
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = conn.cursor()
            
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipping (
                shipping_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                next_shipment_date DATE NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """)
            
           
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                
                products = [
                    ("Laptop", "High-performance business laptop", 999.99),
                    ("Smartphone", "Latest model smartphone", 699.99),
                    ("Headphones", "Noise-cancelling wireless headphones", 249.99),
                    ("Tablet", "10-inch Android tablet", 349.99),
                    ("Smartwatch", "Fitness tracking smartwatch", 199.99)
                ]
                
                for product in products:
                    cursor.execute(
                        "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
                        product
                    )
                    product_id = cursor.lastrowid
                    
                    
                    quantity = (product_id * 5) + 3 
                    cursor.execute(
                        "INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)",
                        (product_id, quantity)
                    )
                    
                   
                    next_shipment = datetime.now() + timedelta(days=product_id * 2)
                    cursor.execute(
                        "INSERT INTO shipping (product_id, next_shipment_date) VALUES (%s, %s)",
                        (product_id, next_shipment)
                    )
            
            conn.commit()
            print("Database initialized successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

