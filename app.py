from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPassword",
    database="registered_vehicles"
)

if db.is_connected():
    print("Connected to the database")
else:
    print("Failed to connect to the database")



cursor = db.cursor()

@app.route('/')
def index():
    # Fetch data from the database
    cursor.execute("SELECT * FROM Vehicle")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return render_template('index.html', columns=columns, data=data)

if __name__ == '__main__':
    app.run(debug=True)
