# app/db/executor.py
import mysql.connector


def execute_query(sql):
    conn = mysql.connector.connect(
        host="localhost", user="root", password="mysql@123", database="rbac_demo"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
