import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="simplegh1023",
    database="server_logs"
)

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
