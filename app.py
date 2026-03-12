import streamlit as st
import pymongo
import hashlib
import os
from dotenv import load_dotenv

# System Configuration
st.set_page_config(page_title="Student Performance Prediction System", page_icon="🔐", layout="centered")

# Initialize environment variables for local fallback
load_dotenv()

# Unified Configuration Function
def get_config(key):
    # Check Streamlit Secrets
    if key in st.secrets:
        return st.secrets[key]
    # Check Environment Variables
    return os.getenv(key)

# Retrieve and validate MONGO_URI
MONGO_URI = get_config("MONGO_URI")

# Database Connection Execution
@st.cache_resource
def init_connection():
    if not MONGO_URI:
        st.error("Configuration Error: MONGO_URI not found in Secrets or .env file.")
        st.stop()
    return pymongo.MongoClient(MONGO_URI)

try:
    client = init_connection()
    # Ping database to verify connection establishment
    client.admin.command('ping')
    db = client["student_performance_db"]
    users_collection = db["users"]
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# Cryptographic Hash Function
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Session State Initialization
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Authentication Logic
def authenticate_user(username, password):
    hashed_pwd = hash_password(password)
    user = users_collection.find_one({"username": username, "password": hashed_pwd})
    if user:
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        st.switch_page("pages/1_Dashboard.py")
    else:
        st.error("Authentication failed. Invalid credentials.")

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        st.warning("User entity already exists.")
        return
    hashed_pwd = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_pwd})
    st.success("Registration successful. Execute login.")

# User Interface Generation
if st.session_state['authenticated']:
    # Immediate redirect if session is active
    st.switch_page("pages/1_Dashboard.py")
else:
    st.title("System Authentication Gateway")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        st.subheader("Administrator Access")
        login_username = st.text_input("Username", key="log_user")
        login_password = st.text_input("Password", type="password", key="log_pass")
        if st.button("Authenticate"):
            authenticate_user(login_username, login_password)
            
    with tab_register:
        st.subheader("Initialize New Administrator")
        reg_username = st.text_input("New Username", key="reg_user")
        reg_password = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if reg_username and reg_password:
                register_user(reg_username, reg_password)
            else:
                st.error("Input fields cannot be null.")
