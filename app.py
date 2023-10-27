from flask import Flask, render_template, request, jsonify
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
    return render_template('index2.html')

@app.route('/execute_query')

def execute_query():
    try:
        query = request.args.get('query')
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        result = cursor.fetchall()
        return render_template('index2.html', columns=columns, rows=result, query=query)
    except mysql.connector.Error as error:
        return render_template('index2.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
