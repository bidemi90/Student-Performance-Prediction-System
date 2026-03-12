import streamlit as st
import pandas as pd
import joblib
import pymongo
import os
from dotenv import load_dotenv

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

# Data Availability Verification
if 'raw_data' not in st.session_state:
    st.warning("No dataset detected in system memory. Execute Data Ingestion module first.")
    st.stop()

# Page Configuration
st.set_page_config(page_title="Risk Predictions", page_icon="⚙️", layout="wide")
st.title("Modular Ensemble Execution")
st.markdown("---")

# Database Connection Initialization
@st.cache_resource
def init_connection():
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in Secrets or .env file.")
    return pymongo.MongoClient(MONGO_URI)

try:
    client = init_connection()
    db = client["student_performance_db"]
    predictions_collection = db["predictions"]
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# Model Loading Execution
@st.cache_resource
def load_model():
    model_path = os.path.join("ml", "models", "student_model.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_model()

if model is None:
    st.error("Intelligence Tier Error: 'student_model.pkl' file not located at 'ml/models/student_model.pkl'.")
    st.stop()

st.success("Intelligence Tier Active: Voting Classifier model loaded successfully.")

# Data Retrieval
df = st.session_state['raw_data'].copy()

# Feature Engineering (Target and Identifier Exclusion)
columns_to_drop = []
if 'ExamScore' in df.columns:
    columns_to_drop.append('ExamScore')
if 'StudentID' in df.columns:
    columns_to_drop.append('StudentID')

if columns_to_drop:
    X_predict = df.drop(columns=columns_to_drop)
    st.info(f"System Action: Features {columns_to_drop} isolated and removed from inference matrix.")
else:
    X_predict = df.copy()

# Prediction Execution
if st.button("Execute Risk Prediction Engine"):
    with st.spinner("Executing ensemble model inference..."):
        try:
            # Generate predictions
            predictions = model.predict(X_predict)
            
            # Map numeric output to categorical labels
            if pd.api.types.is_numeric_dtype(predictions):
                label_mapping = {0: "At-Risk", 1: "Average", 2: "Good", 3: "Excellent"}
                mapped_predictions = [label_mapping.get(p, "Unknown") for p in predictions]
                df['Risk_Label'] = mapped_predictions
            else:
                df['Risk_Label'] = predictions
                
            st.session_state['scored_data'] = df
            
            st.success("Prediction execution complete. Results generated.")
            
            # Database Ingestion
            records_to_insert = df.to_dict('records')
            
            # Clear existing records to prevent duplication
            predictions_collection.delete_many({})
            
            # Insert new batch
            predictions_collection.insert_many(records_to_insert)
            st.info(f"Database Synchronization: {len(records_to_insert)} records committed to MongoDB.")
            
        except Exception as e:
            st.error(f"Inference execution failed: {e}")

# Result Visualization
if 'scored_data' in st.session_state:
    st.subheader("Prediction Results Matrix")
    
    # Filter controls
    risk_filter = st.multiselect(
        "Filter by Risk Classification",
        options=st.session_state['scored_data']['Risk_Label'].unique(),
        default=st.session_state['scored_data']['Risk_Label'].unique()
    )
    
    filtered_df = st.session_state['scored_data'][st.session_state['scored_data']['Risk_Label'].isin(risk_filter)]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Export capability
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Scored Dataset (CSV)",
        data=csv,
        file_name='scored_student_predictions.csv',
        mime='text/csv',
    )
