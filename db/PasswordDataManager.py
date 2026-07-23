import psycopg

# Define your connection string
class PasswordDataManager:
    def __init__(self):
        self.connection = psycopg.connect(
            host="localhost",
            dbname="tianshan",
            user="developer",
            password="meiyou",
            port=5432
        )
        print("Successfully connected to PostgreSQL.")
    def close(self):
        self.connection.close()
        print("Successfully closed connection to PostgreSQL.")
    def convert_to_dict(self,t1,t2):
        l1 = list(t1)
        l2 = list(t2)
        my_dict = {}
        for x in range(len(l1)):
            my_dict[l1[x]] = l2[x]
        return my_dict
    def convert_to_list(self,key_tuple,list_of_tuple):
        my_list = []
        for x in range(len(list_of_tuple)):
            my_list.append(self.convert_to_dict(key_tuple,list_of_tuple[x]))
        return my_list
    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password (
                    key TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    description TEXT
                );
            """)
            self.connection.commit()  # Commit changes to save them
        print("Table Successfully created.")

    def add_password(self, key,username, password, description):
        item = self.retrieve_password(key)
        if item == None:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO password (key,username, password, description)
                VALUES (%s,%s, %s, %s)
                """, (key,username, password, description))
                self.connection.commit()
    def retrieve_password(self, key):
        print("Query password table with key=" + key)
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM password WHERE key = %s
            """,(key,))
            # rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            if cursor.rowcount == 0:
                return None
            else:
                return self.convert_to_dict(("key","username","password","description"),cursor.fetchone())
    def retrieve_all_passwords(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT key,username,password,description FROM password
            """)
            return self.convert_to_list(("key","username","password","description"),cursor.fetchall())
    def update_password(self, key, username, password, description):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            UPDATE password SET username = %s,password = %s,description = %s WHERE key = %s
            """, (username, password, description, key))
            self.connection.commit()
    def delete_password(self, key):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM password WHERE key = %s
            """,(key,))
            self.connection.commit()

# Instantiate the single, shared instance here
singleton_config = PasswordDataManager()
