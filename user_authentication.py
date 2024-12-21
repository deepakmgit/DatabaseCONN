import streamlit as st
import mysql.connector
import hashlib

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="Deepak@26",  # Replace with your MySQL password
        database="Demo"  # Replace with your database name
    )

# Helper functions
def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_cred_table():
    """Create the user_cred table if it doesn't exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_cred (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user_to_cred(username, password):
    """Add a new user to the user_cred table."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute('INSERT INTO user_cred (name, password) VALUES (%s, %s)', 
                       (username, hashed_password))
        conn.commit()
        st.success("User created successfully!")
    except mysql.connector.IntegrityError:
        st.error("Username already exists!")
    finally:
        conn.close()

def authenticate_user_from_cred(username, password):
    """Authenticate a user by verifying their credentials in user_cred."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM user_cred WHERE name = %s', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] == hash_password(password)
    return False

# Main app
def main():
    st.title("MySQL User Authentication App (user_cred)")

    # Initialize the database
    create_user_cred_table()

    # Navigation menu
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if authenticate_user_from_cred(username, password):
                st.success(f"Welcome, {username}!")
                # Add restricted content here
                st.write("You are now logged in.")
            else:
                st.error("Invalid username or password!")

    elif choice == "Sign Up":
        st.subheader("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if new_password == confirm_password:
                add_user_to_cred(new_username, new_password)
            else:
                st.error("Passwords do not match!")

if __name__ == "__main__":
    main()
