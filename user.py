import streamlit as st
import sqlite3
import sys
import xml.etree.ElementTree as ET
import mysql.connector
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import random
import string
from main import user_details, authenticate_user
# from multiapp import MultiApp


def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yogadeepa@210",
        database="registered_vehicles"
    )
    return db

# get all tables of database


def get_tables(cursor, operation):
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]
    if operation == 'Update data':
        relevant_tables = ['owners', 'insurance','credentials']
        return [table for table in tables if table in relevant_tables]
    if operation == 'Insert data':
        relevant_tables = ['maintenance']
        return [table for table in tables if table in relevant_tables]
    else:
        return tables


# function to get column names


def get_column_names(db, table_name):
    query = f"SELECT * FROM {table_name} LIMIT 0"
    df = pd.read_sql_query(query, db)
    columns = df.columns
    print(columns)
    return columns


# get data of a table
def fetch_all_data(conn, table, owner_id):

    owner_id_tables = ['owners', 'registration',
            'license', 'vehicle', 'insurance']
    vehicle_id_tables = ['violation', 'accident', 'maintenance', 'inspection']

    cursor = conn.cursor()

    # call the stored procedure
    print(table, owner_id)
    if table in owner_id_tables:
        query = f"SELECT * FROM {table} WHERE owner_id = {owner_id}"
        # result = pd.read_sql_query(query, conn)
    
    if table == 'credentials':
        query = f"SELECT * from credentials WHERE  username = {owner_id}"
    if table in vehicle_id_tables:
        if table == 'violation':
            query = f"SELECT violation.Violation_id, violation.Fine_amount, violation.violation_date, violation.violation_type, vehicle.RegNumber, vehicle.Model, vehicle.NumberPlate, vehicle.VehicleType, owners.Owner_name, owners.Owner_phone FROM violation JOIN vehicle ON violation.Vehicle_id = vehicle.Vehicle_id JOIN owners ON vehicle.Owner_id = owners.Owner_id WHERE owners.Owner_id = {owner_id}"
        elif table == 'accident':
            query = f"SELECT accident.Accident_id, accident.Location, accident.Accident_date, accident.Accident_description, vehicle.RegNumber, vehicle.Model, vehicle.Reg_year, vehicle.NumberPlate, vehicle.VehicleType, vehicle.Vehicle_description, owners.Owner_name, owners.Owner_phone, owners.Owner_mail, owners.Gender, owners.Address, owners.Dob FROM accident JOIN vehicle ON accident.Vehicle_id = vehicle.Vehicle_id JOIN owners ON vehicle.Owner_id = owners.Owner_id WHERE owners.Owner_id = {owner_id}"
        elif table == 'maintenance':
            query = f"SELECT maintenance.Service_id, maintenance.Service_cost, maintenance.Service_date, maintenance.Next_Service_date, maintenance.Details, vehicle.RegNumber, vehicle.Model, vehicle.NumberPlate, vehicle.VehicleType, owners.Owner_name, owners.Owner_phone FROM maintenance JOIN vehicle ON maintenance.vehicle_id = vehicle.vehicle_id JOIN owners ON vehicle.owner_id = owners.owner_id WHERE owners.owner_id = {owner_id}"
        elif table == 'inspection':
            query = f"SELECT inspection.Inspection_id, inspection.Result, inspection.Inspection_date, vehicle.RegNumber, vehicle.Model, vehicle.NumberPlate, vehicle.VehicleType, owners.Owner_name, owners.Owner_phone FROM inspection JOIN vehicle ON inspection.vehicle_id = vehicle.vehicle_id JOIN owners ON vehicle.owner_id = owners.owner_id WHERE owners.owner_id = {owner_id}"
    # else:
    #     cursor.callproc('DisplayOwnerDetails', [table, owner_id])
    #     # Fetch the result
    #     result = None
    #     for result_cursor in cursor.stored_results():
    #         result = result_cursor.fetchall()

    #     cursor.execute(
    #         f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
    #     column_names = [column[0] for column in cursor.fetchall()]

    #     # Combine column names with data
    #     result = [dict(zip(column_names, row)) for row in result]
    #     return result
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# Function to add a new row to the database
def insert_data(db, cursor, table, column):
    st.write(f'Inserting data for {table}. Enter new values:')
    new_values = {}

    # Generate a random Service ID
    service_id = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8))
    new_values['Service_id'] = service_id

    # Display a calendar for Service_date and Next_Service_date
    new_values['Service_date'] = st.date_input('Select Service Date:')
    new_values['Next_Service_date'] = st.date_input(
        'Select Next Service Date:')

    # Get other values from the user
    new_values['Details'] = st.text_area('Enter Details:')
    columns = get_column_names(db, table)
    for column in columns:
        if column not in ['Service_date', 'Next_Service_date', 'Service_id', 'Details', 'vehicle_id']:
            new_values[column] = st.text_input(f'Enter {column}:')

    # Construct the insert query
    insert_query = f"INSERT INTO {table} ("
    insert_query += ', '.join(new_values.keys())
    insert_query += ") VALUES ("
    insert_query += ', '.join(['%s' for _ in new_values])
    insert_query += ")"

    # Display the generated Service ID to the user
    st.write(f'Generated Service ID: {service_id}')

    insert_button = st.button('Insert')
    if insert_button:
        # Flatten the values into a tuple
        values = [new_values[column] for column in new_values]
        cursor.execute(insert_query, values)
        db.commit()
        st.success(f'Data inserted successfully for {table}.')
    db.commit()


# Function to update data in the database
# Function to update data in the database
def update_data(db, cursor, table, columns, owner_id):

    # Get columns dynamically
    columns = get_column_names(db, table)

    if table == 'owners':
        # Allow users to update their phone number, address, and email
        new_phone = st.text_input('Enter new phone number:')
        new_address = st.text_input('Enter new address:')
        new_email = st.text_input('Enter new email:')

        # Perform the update only for the current owner
        update_query = f"UPDATE {table} SET Owner_phone = %s, Address = %s, owner_mail = %s WHERE owner_id = %s"
        cursor.execute(
            update_query, (new_phone, new_address, new_email, owner_id))

        update_button = st.button('Update')
        if update_button:
            db.commit()
            st.success(f'Data updated successfully for {table}.')
        
    if table == 'credentials':
        old_pass = st.text_input('Enter old password:',type='password')
        query = f'SELECT password from credentials WHERE username = {owner_id}'
        cursor.execute(query)
        result = cursor.fetchone()
        if result:  # If a record with the given username is found
            stored_password = result[0]
            if old_pass == stored_password:
                new_pass = st.text_input('Enter new password:',type='password')
                confirm_pass = st.text_input('Confirm new password:',type='password')
                if new_pass and confirm_pass:
                    if new_pass == confirm_pass:
                        update_query = f"UPDATE credentials SET password = '{new_pass}' WHERE username = {owner_id}"
                        cursor.execute(update_query)
                        print("---------->",update_query)
                        if st.button('Update'):
                            db.commit()
                            st.success("Password updated successfully!")
                    else:
                       st.error("Passwords don't match. Please try again.")
            else:
                st.warning("Incorrect password entered. Please try again.")      
        

    elif table == 'insurance':
        # Allow users to update all columns
        st.write(f'Updating data for {table}. Enter new values:')
        new_values = {}
        vehicle_id = st.text_input('Enter the Vehicle ID:')
        vehicle_id = f"'{vehicle_id}'"
        # Display a calendar for insurance_expiry
        new_values['Insurance_expiry'] = st.date_input(
            'Select Insurance Expiry Date:')
        for column in columns:
            if column != 'Owner_id' and column != 'Insurance_expiry' and column != 'Vehicle_id':
                new_values[column] = st.text_input(f'Enter new {column}:')

        # Construct the update query
        update_query = f"UPDATE {table} SET "
        update_query += ', '.join([f"{column} = %s" for column in new_values])
        update_query += f" WHERE owner_id = {owner_id} AND Vehicle_id = {vehicle_id}"

        update_button = st.button('Update')
        if update_button:
            # Flatten the values into a tuple
            values = [new_values[column] for column in new_values]
            # values.extend([owner_id, vehicle_id])
            # print(values)
            # print(update_query)
            cursor.execute(update_query, values)
            db.commit()
            st.success(f'Data updated successfully for {table}.')


# handle different operations on table
def handle_table(db, cursor, table, owner_id, option):

    columns = get_column_names(db, table)

    if option == 'View data':
        # Display all data in table
        st.subheader(f'{table} data:')
        table_data = fetch_all_data(db, table, owner_id)
        if table_data:
            st.dataframe(table_data)
        else:
            st.warning('No Data Found')

    elif option == 'Insert data':
        # Add a new vehicle
        st.subheader('Add a New row')
        insert_data(db, cursor, table, columns)

    elif option == 'Update data':
        st.subheader('Update data')
        update_data(db, cursor, table, columns, owner_id)

    return

# Streamlit app


def user_dashboard():
    print(user_details)
    username = None
    password = None
    for i in user_details:
        username = i
        password = user_details[i]
    if authenticate_user(username, password):
        st.title('User Dashboard - Vehicle Management System')
        owner_id = st.text_input('Enter the Owner ID:')
        if owner_id in user_details.keys():
            db = connect_db()
            cursor = db.cursor()
            option = st.sidebar.selectbox(
                'Select Operation', ['View data', 'Update data', 'Insert data'])
            tables = get_tables(cursor, option)
            table = st.sidebar.selectbox('Select Table', tables)
            owner_id = f"'{owner_id}'"
            handle_table(db, cursor, table, owner_id, option)
            db.close()
        else:
            st.warning("Owner ID does not match with the login user ID")
    else:
        st.warning("Please Log In with your Owner ID to access the page.")


if __name__ == '__main__':
    st.set_page_config(
        page_title="AutoMate",
        page_icon="🚗",
        layout="wide",
    )
    user_dashboard()
