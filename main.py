import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to establish a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Deepak@26",
            database="Demo"
        )
        st.success("Connected to the database successfully!")
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch data from the database
def fetch_data(query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to insert data into the database
def insert_data(query, values, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        st.success("Data inserted successfully!")
    except Error as e:
        st.error(f"Error inserting data: {e}")
        connection.rollback()

# Streamlit app
st.title("MySQL Database Viewer and Inserter")

# Input form for database credentials
with st.form("db_form"):
    st.header("Database Connection Settings")
    host = st.text_input("Host", "localhost")
    user = st.text_input("User", "root")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database Name")
    query = st.text_area("SQL Query", "SELECT * FROM your_table LIMIT 10")
    submitted = st.form_submit_button("Connect and Fetch Data")

# Form for inserting data
with st.form("insert_form"):
    st.header("Insert Data into Table")
    table_name = st.text_input("Table Name")
    columns = st.text_input("Columns (comma separated)", "column1, column2, column3")
    values = st.text_input("Values (comma separated)", "value1, value2, value3")
    insert_submitted = st.form_submit_button("Insert Data")

if submitted:
    # Connect to the database
    conn = create_connection(host, user, password, database)
    if conn:
        # Fetch and display data
        data = fetch_data(query, conn)
        if data:
            st.write("Query Results:")
            st.write(data)

        # Close the database connection
        conn.close()
        st.info("Database connection closed.")

if insert_submitted:
    # Connect to the database
    conn = create_connection(host, user, password, database)
    if conn:
        # Prepare the insert query and values
        columns_list = columns.split(",")
        values_list = values.split(",")
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_list)}) VALUES ({', '.join(['%s'] * len(values_list))})"
        
        # Insert data
        insert_data(insert_query, tuple(values_list), conn)

        # Close the database connection
        conn.close()
        st.info("Database connection closed.")
