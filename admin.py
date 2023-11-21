import streamlit as st
import sqlite3
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from main import admin_details, authenticate_admin
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import random
import warnings
warnings.filterwarnings("ignore")

def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yogadeepa@210",
        database="registered_vehicles"
    )

    return db

# get all tables of database
def get_tables(cursor,operation):
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]

    if operation == "Update data" :
        relevant_tables = ['accident','inspection','insurance','license','maintenance','owners','registration','vehicle','violation']
        return [table for table in tables if table in relevant_tables]

    if operation == "Insert data":
        relevant_tables = ['accident','violation']
        return [table for table in tables if table in relevant_tables]
    
    return tables

# function to get column names


def get_column_names(db, table_name):
    query = f"SELECT * FROM {table_name} LIMIT 0"
    df = pd.read_sql_query(query, db)
    columns = df.columns
    print(columns)
    return columns


# get data of a table
def fetch_all_data(conn, table):
    cursor = conn.cursor()

    # call the stored procedure
    cursor.callproc('get_table_data', [table])
    # Fetch the result
    result = None
    for result_cursor in cursor.stored_results():
        result = result_cursor.fetchall()
        
    cursor.execute(
        f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
    column_names = [column[0] for column in cursor.fetchall()]

    # Combine column names with data
    result = [dict(zip(column_names, row)) for row in result]

    return result

# Function to generate random alphanumeric ID
def generate_random_id():
    return str(uuid.uuid4().hex.upper()[0:4])

def gen_random_license():
    return str(random.randint(10000, 99999))

def gen_random_reg():
    return str(uuid.uuid4().hex.upper()[0:6])

def gen_random_insp():
    return str(uuid.uuid4().hex.upper()[0:4])

def gen_random_accident_id():
    return str(uuid.uuid4().hex.upper()[0:3])


def fetch_owner_id_by_license(cursor, license_num):
    query = "SELECT owner_id FROM license WHERE License_number = %s"
    cursor.execute(query, (license_num,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def fetch_vehicles_by_owner(cursor, owner_id):
    query = "SELECT Vehicle_id, NumberPlate FROM vehicle WHERE owner_id = %s"
    cursor.execute(query, (owner_id,))
    results = cursor.fetchall()
    if results:
        return results
    else:
        return None

# Function to add a new row to the database
def insert_data(db, cursor, table, column):
    st.subheader('Insert New Record')
    if table == 'accident':
        acc_id = 'ACC'+gen_random_accident_id()
        license_num = st.text_input('License Number')

        # Fetch owner_id from the database based on the provided license_num
        owner_id = fetch_owner_id_by_license(cursor, license_num)

        if owner_id:
            # Fetch list of vehicles associated with the owner
            vehicles = fetch_vehicles_by_owner(cursor, owner_id)

            if vehicles:
                # Create a list of vehicle options for the dropdown
                vehicle_options = [f"{vehicle[0]} - {vehicle[1]}" for vehicle in vehicles]

                # Allow admin to choose from the list of vehicles
                selected_vehicle = st.selectbox('Select Vehicle', vehicle_options)

                # Extract vehicle_id from the selected option
                vehicle_id = selected_vehicle.split(' - ')[0]

                location = st.text_input('Location of Accident')
                acc_date = st.date_input('Accident Date')
                acc_desc = st.text_input('Description about the Accident')

                add_cols = [acc_id, license_num, vehicle_id, location, acc_date, acc_desc]
                if st.button('Add data'):
                    if add_cols:
                        insert_query = "INSERT INTO accident VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(insert_query, add_cols)
                        st.success('Details added successfully!')
                    else:
                        st.warning('Please fill in all the details.')
            else:
                st.warning(f'No vehicles found for the owner with ID: {owner_id}')
        else:
            if license_num:
                st.warning(f'No owner found for the given license number: {license_num}')

    elif table == 'violation':
        violation_id = gen_random_insp()
        Vehicle_id = st.text_input('Vehicle ID')
        fine_amt = st.number_input('Fine amount')
        violation_date = st.date_input('Violation Date')
        violation_type = st.text_input('Vioilation Type')
        st.success(f"Generated Violation ID: {violation_id}")


        add_cols = [violation_id,Vehicle_id, fine_amt,violation_date, violation_type]
        
        if st.button('Add data'):
            if add_cols:
                insert_query = "INSERT INTO violation VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, add_cols)
                st.success('Details added successfully!')
            else:
                st.warning('Please fill in all the details.')
    
    db.commit()

def fetch_vehicle_ids_by_owner(cursor, owner_id):
    query = "SELECT Vehicle_id FROM Vehicle WHERE Owner_id = %s"
    cursor.execute(query, (owner_id,))
    result = cursor.fetchall()
    if result:
        return [row[0] for row in result]
    else:
        return []

def delete_data(db, cursor):
    owner_id = st.text_input('Enter Owner ID')
    vehicle_ids = fetch_vehicle_ids_by_owner(cursor, owner_id)

    if vehicle_ids:
        selected_vehicle_id = st.selectbox('Select Vehicle ID to Delete', vehicle_ids)

        if st.button('Delete Vehicle Data'):
            try:
                # Delete data from child tables first
                cursor.callproc('DeleteVehicleDetails', [selected_vehicle_id])
                # print(selected_vehicle_id)
                st.success(f'Data for Vehicle ID {selected_vehicle_id} deleted successfully!')
                db.commit()

            except Exception as e:
                st.warning(f'Error: {e}')

    else:
        if owner_id:
            st.warning(f'No vehicles found for Owner ID: {owner_id}')

def fetch_data(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result
            

def update_data(db, cursor, table, column):
    #code here!
    st.subheader(f'Update {table} Data')
    # Display existing data
    st.write("Existing Data:")

    existing_data = fetch_all_data(db, table)
    existing_data = pd.DataFrame(existing_data)
    st.table(existing_data)

    details = {"owners":"owner_id","accident":"accident_id","insurance":"policy_number",
               "inspection":"inspection_id","license":"license_number","maintenance":"service_id",
               "registration":"register_id","vehicle":"vehicle_id","violation":"violation_id"}
    # Choose the record to update
    record_id = st.text_input(f'Enter {details[table]} to Update')
    if not record_id:
        st.warning('Please enter a valid ID to update.')
        return

    # Display update options
    st.write("Update Options:")
    update_options = {}
    for col in column:
        update_options[col] = st.text_input(f'Update {col}')
    update_options = {k: v for k, v in update_options.items() if v}  # Remove empty values

    # Update the record
    if st.button('Update Data'):
        try:
            set_clause = ", ".join([f"{col} = %s" for col in update_options.keys()])    
            update_query = f"UPDATE {table} SET {set_clause} WHERE {details[table]}= %s"
            print(update_query)
            update_values = list(update_options.values()) + [record_id]
            cursor.execute(update_query, update_values)
            db.commit()
            st.success(f'Data for {table} ID {record_id} updated successfully!')
        except Exception as e:
            st.warning(f'Error: {e}')


def validate_email(email):
    return '@' in email


def insert_new_details(db,cursor):
    st.subheader('Insert New Details')
    # Insert details for owners
    st.subheader('Owner Details:')
    owner_id = generate_random_id()
    owner_name = st.text_input('Owner Name')
    owner_phone = st.text_input('Owner Phone number')
    if owner_phone:
        if len(owner_phone) != 10 or not owner_phone.isdigit():
            st.warning('Invalid phone number format. Please enter a 10-digit number.')
            return
    owner_mail = st.text_input('Owner Mail')
    if owner_mail:
        if not validate_email(owner_mail):
            st.warning('Invalid email format. Please enter a valid email.')
            return
        

    license_num = 'LIC' + gen_random_license()
    gender = st.selectbox('Gender', ['M', 'F'])
    address = st.text_area('Address')
    dob = st.date_input('Date of Birth', min_value=datetime(1930, 1, 1))
    age = (datetime.now().date() - dob).days // 365
    if age <= 18:
        st.warning('Owner must be at least 18 years old.')
        return
    
    st.success(f"Generated Owner ID: {owner_id}")
    st.success(f"Generated License Number: {license_num}")

    owner_data = [owner_id, owner_name, owner_phone, license_num, owner_mail, gender, address, dob]

    # Insert details for vehicle
    st.subheader('Vehicle Details:')
    Vehicle_id = st.text_input('Vehicle ID')
    RegNumber = 'REG' + gen_random_insp()
    NumberPlate = st.text_input('Number plate')
    RegDate = st.date_input('Registration Date')
    model = st.text_input('Model')

    # Use the generated owner ID
    VehicleType = st.text_input('Vehicle Type (Motorcycle / Car)')
    Vehicle_description = st.text_area('Vehicle Description')

    vehicle_data = [Vehicle_id,RegNumber,model, owner_id, RegDate,NumberPlate, VehicleType, Vehicle_description]

    # Insert details for license
    st.subheader('License Details:')
    issue_date = st.date_input('Issue Date')
    exp_date = st.date_input('Expiration Date')

    license_data = [license_num, owner_id, issue_date, exp_date, VehicleType]

    # Insert details for registration
    st.subheader('Registration Details:')
    reg_id = 'REG' + gen_random_reg()
    reg_date = RegDate
    renewal_date = st.date_input('Renewal Date')
    st.success(f"Generated Registration ID: {reg_id}")

    registration_data = [reg_id, Vehicle_id, owner_id, reg_date, renewal_date]

    # Insert details for inspection
    st.subheader('Inspection Details:')
    insp_id = 'INSP' + gen_random_insp()
    insp_name = st.text_input('Inspector Name')
    result = st.text_input('Result of the Inspection (1 for Positive result and 0 for Negative result)')
    insp_date = st.date_input('Inspection Date')
    st.success(f"Generated Inspection ID: {insp_id}")

    inspection_data = [insp_id, insp_name, result, insp_date, Vehicle_id]

    # Display data before inserting
    if st.button('Display Data'):
        st.subheader('Owner Data:')
        st.table(owner_data)

        st.subheader('Vehicle Data:')
        st.table(vehicle_data)

        st.subheader('License Data:')
        st.table(license_data)

        st.subheader('Registration Data:')
        st.table(registration_data)

        st.subheader('Inspection Data:')
        st.table(inspection_data)

    # Insert data into the tables in the specified order
    if st.button('Insert Data'):
        try:
            # Insert into owners table
            insert_query_owners = "INSERT INTO owners VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query_owners, owner_data)

            # Insert into vehicle table
            insert_query_vehicle = "INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query_vehicle, vehicle_data)

            # Insert into license table
            insert_query_license = "INSERT INTO license VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query_license, license_data)

            # Insert into registration table
            insert_query_registration = "INSERT INTO registration VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query_registration, registration_data)

            # Insert into inspection table
            insert_query_inspection = "INSERT INTO inspection VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query_inspection, inspection_data)

            st.success('Data inserted successfully!')
            db.commit()
        except Exception as e:
            st.warning(f'Error: {e}')



# handle different operations on table
def handle_table(db, cursor,option):

    tables = get_tables(cursor,option)
    if option == 'Insert data':
        tables.append("new details")
    
    if option == 'View data':
        table = st.sidebar.selectbox('Select Table', tables)
        # Display all data in table
        st.subheader(f'{table} data:')
        table_data = fetch_all_data(db, table)
        st.dataframe(table_data)

    elif option == 'Insert data':
        table = st.sidebar.selectbox('Select Table', tables)
        # Add a new vehicle
        if table == 'accident' or table == 'violation':
            columns = get_column_names(db, table)
            insert_data(db, cursor, table, columns)
        elif table == 'new details':
            insert_new_details(db, cursor)

    elif option == 'Delete data':
        delete_data(db, cursor)

    elif option == 'Analyze data':
        analyze(cursor)

    elif option == 'Update data':
        table = st.sidebar.selectbox('Select Table', tables)
        columns = get_column_names(db, table)
        # st.subheader('Update data')
        update_data(db, cursor, table, columns)
    return

def fetch_accidents_by_month(cursor):
    query = """
    SELECT MONTH(Accident_date) AS Month, COUNT(*) AS Count
    FROM accident
    GROUP BY MONTH(Accident_date)
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return pd.DataFrame(results, columns=['Month', 'Count'])


def fetch_violations_by_month(cursor):
    query = """
    SELECT MONTH(violation_date) AS Month, COUNT(*) AS Count
    FROM violation
    GROUP BY MONTH(violation_date)
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return pd.DataFrame(results, columns=['Month', 'Count'])
 
def analyze(cursor):
        st.empty()
        query = "SELECT Gender, COUNT(*) as Count FROM owners GROUP BY Gender"
        cursor.execute(query)
        results = cursor.fetchall()

        # Create a DataFrame for visualization
        df = pd.DataFrame(results, columns=['Gender', 'Count'])
        # st.table(df)
        st.set_option('deprecation.showPyplotGlobalUse', False)


        # Plot the bar graph using Seaborn
        plt.figure(figsize=(4, 2))
        sns.barplot(x='Gender', y='Count', data=df, linewidth=2, edgecolor="0.2", color='skyblue')
        plt.title('Number of Male and Female Drivers')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.xticks([0, 1], ['Male', 'Female'])  # Assuming 0 for Male and 1 for Female
        st.pyplot()

        accidents_by_month = fetch_accidents_by_month(cursor)
        # Plot the bar chart
        plt.figure(figsize=(4, 2))
        sns.barplot(x='Month', y='Count', data=accidents_by_month, linewidth=2, edgecolor="0.2", color='skyblue')
        plt.title('Number of Accidents by Month')
        plt.xlabel('Month')
        plt.ylabel('Count')
        st.pyplot()
        violations_by_month = fetch_violations_by_month(cursor)
        # Plot the bar chart
        plt.figure(figsize=(4, 2))
        sns.barplot(x='Month', y='Count', data=violations_by_month, linewidth=2, edgecolor="0.2", color='skyblue')
        plt.title('Number of Violations by Month')
        plt.xlabel('Month')
        plt.ylabel('Count')

        # Display the plot in the Streamlit app
        st.pyplot()

    

# Streamlit app
def admin_dashboard():
    username = None
    password = None
    for i in admin_details:
        username = i
        password = admin_details[i]
    if authenticate_admin(username, password):
        st.write("Welcome to the Admin page!")
        st.title('Admin Dashboard - Vehicle Management System')
        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # Sidebar menu
        st.sidebar.title('Menu')
        option = st.sidebar.selectbox(
            'Select Operation', ['View data', 'Insert data', 'Update data', 'Delete data','Analyze data'])

        # table = st.sidebar.selectbox('Select Table', tables)

        handle_table(db, cursor,option)
        db.close()
    else:
        st.warning("Please Log In to access the pages.")

if __name__ == '__main__':
    st.set_page_config(
        page_title="AutoMate",
        page_icon="🚗",
        layout="centered",
    )
    admin_dashboard()
