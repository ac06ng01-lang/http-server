import mysql.connector, time

mydb = None
while mydb is None:
    try:
        mydb = mysql.connector.connect(
            host="db",
            user="root",
            password="simplegh1023",
            database="server_logs"
        )
        print("Successfully connected to the MySQL database!")
    except mysql.connector.Error as err:
        print("Database not ready yet, waiting 3 seconds...")
        time.sleep(3)

LOG_TABLES = [
    "request_logs",
    "response_logs",
    "error_logs"
]

INDEX_REQUEST = 0
INDEX_RESPONSE = 1
INDEX_ERROR = 2


def logger(address, data, index):
    if not isinstance(data, str):
        data = ', '.join(data)
    cursor = mydb.cursor()
    values = f"'{address}', '{data}'"

    sql = f"INSERT INTO {LOG_TABLES[index]} VALUES ({values}, CURRENT_TIMESTAMP())"
    cursor.execute(sql)

    mydb.commit()
    print(cursor.rowcount, "was inserted.")
