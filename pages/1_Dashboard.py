import streamlit as st
import pymongo
import pandas as pd
import os
from dotenv import load_dotenv

st.write("Debug - Secrets keys found:", list(st.secrets.keys()))


# Try to load local .env (only works on your PC)
load_dotenv()
# Function to safely get secrets from Streamlit or Local Env
def get_config(key):
    # Check if running on Streamlit Cloud
    if key in st.secrets:
        return st.secrets[key]
    # Fallback to local .env/environment variables
    return os.getenv(key)

# Retrieve and validate MONGO_URI
MONGO_URI = get_config("MONGO_URI")

# Authentication Verification
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Authentication required. Navigate to the main portal to initiate a session.")
    st.stop()

# Page Configuration
st.set_page_config(page_title="System Dashboard", page_icon="📊", layout="wide")
st.title("System Analytics Dashboard")
st.write(f"Active Administrator: {st.session_state['username']}")
st.markdown("---")

# Database Connection Execution
@st.cache_resource
def init_connection():
    # Uses the _URI variable retrieved via get_config
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in Secrets or .env file.")
    return pymongo.MongoClient(MONGO_URI)

try:
    client = init_connection()
    db = client["student_performance_db"]
    # The 'predictions' collection will be populated by the Risk Predictions module
    predictions_collection = db["predictions"] 
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# Data Retrieval
total_predictions = predictions_collection.count_documents({})

if total_predictions == 0:
    st.info("System database currently contains zero prediction records. Proceed to the Data Upload and Risk Predictions modules to populate analytics.")
else:
    # Aggregate Metrics Calculation
    pipeline = [
        {"$group": {"_id": "$Risk_Label", "count": {"$sum": 1}}}
    ]
    risk_distribution = list(predictions_collection.aggregate(pipeline))

    # High-Level Metrics Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students Processed", total_predictions)
    col2.metric("Ensemble Accuracy Baseline", "88.50%")
    col3.metric("Database Status", "Connected")
    
    st.markdown("---")

    # Data Visualization
    if risk_distribution:
        df_risk = pd.DataFrame(risk_distribution)
        df_risk.rename(columns={"_id": "Risk Label", "count": "Student Count"}, inplace=True)
        # Drop entries where Risk Label might be null due to incomplete records
        df_risk.dropna(subset=['Risk Label'], inplace=True) 
        df_risk.set_index("Risk Label", inplace=True)
        
        st.subheader("Student Risk Category Distribution")
        st.bar_chart(df_risk)
        
        st.subheader("Raw Prediction Data (Recent)")
        # Fetch the 100 most recent records
        recent_records = list(predictions_collection.find({}, {"_id": 0}).sort("_id", -1).limit(100))
        df_recent = pd.DataFrame(recent_records)
        st.dataframe(df_recent, use_container_width=True)
