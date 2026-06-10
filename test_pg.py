import psycopg2
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="ronnie",
        password="*@ronnie2026#",
        host="localhost"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
