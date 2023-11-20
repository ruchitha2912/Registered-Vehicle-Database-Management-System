import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import mysql.connector

admin_details = {   
}

user_details = {
}

admin_credentials = {
    'admin': 'admin1234',
}

# Establish a connection to your MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Yogadeepa@210',
    database='registered_vehicles'
)



def authenticate_admin(login_user, passwd):
    if login_user == 'admin' and admin_credentials[login_user] == passwd:
        return True

def authenticate_user(login_user, passwd):
    global user_details
    cursor = db_connection.cursor()
    query2 = "SELECT username, password FROM credentials"
    cursor.execute(query2)
    results = cursor.fetchall()  
    for row in results:
        username, password = row
        user_details[username] = password

    query1 = "SELECT password FROM credentials WHERE username = %s"
    cursor.execute(query1, (login_user,))
    result = cursor.fetchone()

    if result and result[0] == passwd:
        return True

    return False
