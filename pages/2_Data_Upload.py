import streamlit as st
import pandas as pd
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

# Configuration variables (Ready for use if needed in this module)
MONGO_URI = get_config("MONGO_URI")

# Authentication Verification
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Authentication required. Navigate to the main portal to initiate a session.")
    st.stop()

# Page Configuration
st.set_page_config(page_title="Data Ingestion", page_icon="📂", layout="wide")
st.title("Data Ingestion & Preprocessing")
st.markdown("---")

st.subheader("Upload Student Dataset")
st.write("Supported formats: .csv, .xlsx. Ensure the dataset contains the required Behavioral, Psychological, and Academic pillar features.")

# File Uploader component
uploaded_file = st.file_uploader("Select dataset file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Data Extraction
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"File '{uploaded_file.name}' successfully loaded into system memory.")
        
        # Exploratory Data Analysis (EDA) Preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Data Integrity Verification
        st.subheader("Integrity Verification (Section 3.3.1)")
        total_records = len(df)
        missing_values = df.isnull().sum().sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", total_records)
        col2.metric("Total Features", len(df.columns))
        col3.metric("Total Missing Values", missing_values)
        
        if missing_values > 0:
            st.warning("Warning: Dataset contains missing values. Model accuracy may be impacted.")
        else:
            st.info("Validation successful: 100% data integrity confirmed. Zero missing values detected.")
            
        # State Preservation
        st.session_state['raw_data'] = df
        
        # Module Transition
        if st.button("Initialize Modular Prediction Engine"):
            st.switch_page("pages/3_Risk_Predictions.py")
            
    except Exception as e:
        st.error(f"System encountered an error during data extraction: {e}")
else:
    st.info("System awaiting data file input.")
