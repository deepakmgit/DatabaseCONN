import streamlit as st
import mysql.connector
import hashlib

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Deepak@26",
        database="Demo"
    )

# Helper functions
def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user credentials."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM user_cred WHERE name = %s', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] == hash_password(password)
    return False

def list_tables(connection):
    """List all tables in the database."""
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]

def fetch_table_data(table_name, connection):
    """Fetch data from a table."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def insert_data(query, values, connection):
    """Insert data into a table."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        st.success("Data inserted successfully!")
    except mysql.connector.Error as e:
        st.error(f"Error inserting data: {e}")
        connection.rollback()

def delete_data(query, values, connection):
    """Delete data from a table."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        st.success("Data deleted successfully!")
    except mysql.connector.Error as e:
        st.error(f"Error deleting data: {e}")
        connection.rollback()

# Main app
def login_page():
    """Login page for authentication."""
    st.title("User Authentication")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password!")

def operations_page():
    """Operations page after successful authentication."""
    st.title("Database Operations")
    conn = create_connection()

    # Operations Menu
    operations = ["Show Tables", "View Table Data", "Insert Data", "Delete Data"]
    selected_operation = st.radio("Choose an operation", operations)

    if selected_operation == "Show Tables":
        st.subheader("Tables in the Database")
        tables = list_tables(conn)
        if tables:
            st.write(tables)
        else:
            st.write("No tables found.")

    elif selected_operation == "View Table Data":
        st.subheader("View Data from Table")
        table_name = st.selectbox("Select Table", list_tables(conn))
        if table_name:
            data = fetch_table_data(table_name, conn)
            if data:
                st.write(data)
            else:
                st.write("No data available in this table.")

    elif selected_operation == "Insert Data":
        st.subheader("Insert Data into Table")
        table_name = st.text_input("Table Name")
        columns = st.text_input("Columns (comma-separated)", "column1, column2")
        values = st.text_input("Values (comma-separated)", "value1, value2")
        if st.button("Insert"):
            if table_name and columns and values:
                columns_list = columns.split(",")
                values_list = values.split(",")
                query = f"INSERT INTO {table_name} ({', '.join(columns_list)}) VALUES ({', '.join(['%s'] * len(values_list))})"
                insert_data(query, tuple(values_list), conn)

    elif selected_operation == "Delete Data":
        st.subheader("Delete Data from Table")
        del_table = st.text_input("Table Name for Deletion")
        del_condition = st.text_input("Condition for Deletion", "column_name = 'value'")
        if st.button("Delete"):
            if del_table and del_condition:
                query = f"DELETE FROM {del_table} WHERE {del_condition}"
                delete_data(query, None, conn)

    conn.close()

# Manage session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    operations_page()
