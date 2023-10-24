from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="registered_vehicles"
)
if db.is_connected():
    print("Connected to the database")
else:
    print("Failed to connect to the database")
cursor = db.cursor()

@app.route('/')
def index():
    # Display existing data from the database
    cursor.execute("SELECT * FROM owners")
    table_data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    return render_template('index.html', column_names=column_names, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
