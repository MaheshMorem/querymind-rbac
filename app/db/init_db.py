import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="mysql@123")

cursor = conn.cursor()

with open("app/db/init.sql", "r") as f:
    sql_script = f.read()

# Execute multi statements
for result in cursor.execute(sql_script, multi=True):
    pass

cursor.close()
conn.close()

print("✅ Database initialized successfully")
