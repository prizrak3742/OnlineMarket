import pymysql
import pymysql.cursors
from db_config import host, user, password, db_name
import base64

def connection_db(host=host, user=user, password=password, db_name=db_name):
    try:
        conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("Error in connection...")
        print(e)
        return False
    
if __name__ == "__main__":
    conn = connection_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS product_type (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_type VARCHAR(255) NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    price INT NOT NULL,
                    product_type_id INT NOT NULL,
                    description VARCHAR(1566) NOT NULL,
                    user_id INT NOT NULL,
                    photo LONGBLOB
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS account (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    description VARCHAR(1566) NOT NULL,
                    number INT NOT NULL,
                    auth BOOLEAN,
                    host_ads VARCHAR(1566) NOT NULL,
                    photo LONGBLOB
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    comment VARCHAR(1566) NOT NULL,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL
                );
                """
            )
        conn.commit()
        print("Tables created successfully.")
    finally:
        conn.close()

