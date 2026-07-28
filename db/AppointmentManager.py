import psycopg

# Define your connection string
class AppointmentDataManager:
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
                CREATE TABLE IF NOT EXISTS appointment (
                    name TEXT NOT NULL, 
                    start_month TEXT NOT NULL, 
                    start_date TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    event TEXT NOT NULL,
                    info TEXT,
                    PRIMARY KEY (name,start_month,start_date, start_time)
                );
            """)
            self.connection.commit()  # Commit changes to save them
        print("Table p assword Successfully created.")
    def add_appointment(self, name,start_date,start_time, end_time, event):
        start_month = start_date[0:7]
        print("add-start-month==" + start_month)
        with self.connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO appointment(name,start_month,start_date,start_time,end_time,event,info)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (name,start_month,start_date,start_time, end_time, event,"info"))
            self.connection.commit()
    def retrieve_appointment_by_date(self, name,start_date):
        print("Query password table with key=" + start_date)
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT start_date,start_time,end_time,event,info FROM appointment WHERE name = %s and start_date = %s order by start_time
            """,(name,start_date,))
            # rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            if cursor.rowcount == 0:
                return None
            else:
                records = cursor.fetchall()
                return self.convert_to_list(("start_date","start_time","end_time","event","info"),records)
    def retrieve_appointment_by_month(self, name,start_month):
        print("Query password table with key=" + start_month)
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT start_date,start_time,end_time,event,info FROM appointment WHERE name = %s and start_month = %s order by start_date
            """,(name,start_month,))
            # rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            if cursor.rowcount == 0:
                return None
            else:
                records = cursor.fetchall()
                return self.convert_to_list(("start_date","start_time","end_time","event","info"),records)
    def delete_appointment_by_date(self, name,start_date):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM appointment WHERE name = %s and start_date = %s
            """,(name,start_date,))
            self.connection.commit()
    def delete_appointment_by_datetime(self, name,start_date,start_time):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM appointment WHERE name = %s and start_date = %s AND start_time = %s
            """,(name,start_date,start_time))
            self.connection.commit()

# Instantiate the single, shared instance here
singleton_appointment = AppointmentDataManager()
