import streamlit as st
import pandas as pd
import pymongo
import os
from dotenv import load_dotenv

# Authentication Verification
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Authentication required. Navigate to the main portal to initiate a session.")
    st.stop()

# Page Configuration
st.set_page_config(page_title="Student Insights (XAI)", page_icon="🔍", layout="wide")
st.title("Explainable AI (XAI) Student Insights")
st.markdown("---")

# Database Connection Initialization
@st.cache_resource
def init_connection():
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    return pymongo.MongoClient(uri)

try:
    client = init_connection()
    db = client["student_performance_db"]
    predictions_collection = db["predictions"]
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# Data Retrieval
records = list(predictions_collection.find({}, {"_id": 0}))

if not records:
    st.warning("No prediction records found in the database. Execute the Risk Predictions module first.")
    st.stop()

df = pd.DataFrame(records)

# Student Selection Interface
st.subheader("Individual Student Analysis")

# Identify a unique identifier column. Fallback to index if StudentID is missing.
if 'StudentID' in df.columns:
    student_id_list = df['StudentID'].tolist()
    selected_id = st.selectbox("Select Student ID for Deep Dive Analysis", student_id_list)
    student_data = df[df['StudentID'] == selected_id].iloc[0]
else:
    st.info("System Note: 'StudentID' feature not detected. Utilizing system index for selection.")
    student_id_list = df.index.tolist()
    selected_id = st.selectbox("Select Student System Index for Deep Dive Analysis", student_id_list)
    student_data = df.iloc[selected_id]

st.markdown("---")

# Risk Classification Output
risk_label = student_data.get('Risk_Label', 'Unknown')
st.header(f"Predicted Risk Classification: {risk_label}")

# Feature Comparison Logic (XAI Simulation)
# Compares the selected student's metrics against the average metrics of their assigned risk group.
group_avg = df[df['Risk_Label'] == risk_label].mean(numeric_only=True)
student_numeric = student_data[group_avg.index]

# Data Preparation for Visualization
comparison_df = pd.DataFrame({
    'Student Values': student_numeric,
    f'Average for {risk_label} Group': group_avg
})

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Raw Data Metrics")
    st.dataframe(student_data.astype(str), use_container_width=True)

with col2:
    st.subheader("Pillar Variance Analysis")
    st.write("This chart illustrates the student's deviations from their cohort average across all numeric features.")
    st.bar_chart(comparison_df)



# Intervention Recommendations
st.subheader("System-Generated Directives")
if risk_label == "At-Risk":
    st.error("Action Required: High probability of academic failure detected. Immediate counseling intervention recommended focusing on variables with the highest negative variance.")
elif risk_label == "Average":
    st.warning("Action Suggested: Monitor academic progress. Student is performing at baseline parameters.")
elif risk_label in ["Good", "Excellent"]:
    st.success("No Action Required: Student is exceeding baseline parameters.")
else:
    st.info("Classification status indeterminate.")