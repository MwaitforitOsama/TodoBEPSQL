import psycopg2

try:
    # Replace connection parameters with your URL
    conn = psycopg2.connect("postgresql://postgres:admin@localhost:5432/mytodoapp")
    print("Connection successful!")
    
    # Perform database operations here if needed

except psycopg2.Error as e:
    print("Unable to connect to the database:", e)

finally:
    if conn is not None:
        conn.close()
        print("Connection closed.")
