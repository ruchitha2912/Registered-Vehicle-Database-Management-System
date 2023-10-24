import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yogadeepa@210",
        database="registered_vehicles"
    )
    if db.is_connected():
        print("Connected to the database")
    else:
        print("Failed to connect to the database")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    # Handle the error (log it, show an error message, etc.)
finally:
    # Close the database connection (if it was established)
    if 'db' in locals() and db.is_connected():
        db.close()
        print("Database connection closed")

#pip install mysql-connector-python --index-url=https://pypi.org/simple --trusted-host pypi.python.org
#pip download mysql-connector-python
