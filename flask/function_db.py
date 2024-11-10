from db import connection_db

class DataBase:
    def get_ad_by_product(self, product):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM product WHERE product_type_id = {product};")
            return cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.conn.close()
        
    def get_product_by_id(self, id):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM product WHERE id = {id};")
            return cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.conn.close()

    def get_type_by_id(self, id):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT product_type FROM root.product_type where id = {id};")
            return cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.conn.close()

    def create_account(self, name, email, password, description="", number=380, auth=False, host_ads="", photo=None):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM account WHERE email = %s", (email,))
                if cur.fetchone():
                    return ["Email is already registered", "error"]
                
                cur.execute("SELECT * FROM account WHERE number = %s", (number,))
                if cur.fetchone():
                    return ["Number is already registered", "error"]

                cur.execute(
                    "INSERT INTO account (name, email, password, description, number, auth, host_ads, photo) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, email, password, description, number, auth, host_ads, photo)
                )
            self.conn.commit()
            return ["Account created successfully", "success"]
        except Exception as e:
            print(f"Error: {e}")
            return ["Error creating account", "error"]
        finally:
            self.conn.close()

    def get_user(self, id):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM account WHERE id = {id};")
            return cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.conn.close()

    def get_user_by_email(self, email):
        try:
            self.conn = connection_db()
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM account WHERE email = %s", (email,))
                return cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.conn.close()
