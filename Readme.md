# Student Performance Prediction System

## System Overview

The Student Performance Prediction System is a machine learning-based early warning application. It utilizes a **Modular Ensemble architecture** (Voting Classifier) integrating Behavioral, Psychological, and Academic pillars to classify student risk levels. The presentation layer is constructed using **Streamlit**, with session state management and data persistence handled via **MongoDB Atlas**.

## Architecture & Technology Stack

* **Frontend/Interface:** Streamlit (Multipage Application)
* **Machine Learning:** Scikit-learn (Random Forest Classifier, Voting Classifier, Pipeline)
* **Data Manipulation:** Pandas
* **Model Serialization:** Joblib
* **Database:** MongoDB (Atlas via `pymongo`)
* **Environment Management:** `python-dotenv`
* **Media Management:** Cloudinary API

## Project Directory Structure

```text
/ (Project Root Directory)
│
├── app.py                  # Main Streamlit application and Authentication Gateway
├── requirements.txt        # System dependencies
├── .env                    # Environment variables (Sensitive Data)
├── .gitignore              # Files excluded from version control
│
├── /pages                  # Streamlit multipage directory
│   ├── 1_Dashboard.py          # System Analytics Dashboard
│   ├── 2_Data_Upload.py        # Data Ingestion & Preprocessing
│   ├── 3_Risk_Predictions.py   # Modular Ensemble Execution
│   └── 4_Student_Insights.py   # Explainable AI (XAI) Student Insights
│
└── /ml                     # Machine learning directory
    ├── /data
    │   └── student_performance.xlsx
    ├── /models
    │   └── student_model.pkl   # Serialized Voting Classifier (130MB)
    └── /scripts
        └── model_train.py      # Algorithm training script

```

## Prerequisites

1. Python 3.10 or higher installed.
2. Active MongoDB Atlas cloud cluster.
3. Cloudinary Account for media handling.
4. Git Large File Storage (LFS) installed to manage the `.pkl` file.

## Installation Protocol

1. **Clone the repository:**
```bash
git clone <repository_url>
cd student_performance_system

```


2. **Configure Environment Variables:**
Create a `.env` file in the root directory and populate it with your specific credentials:
```text
# Database Configuration
MONGO_URI=your_mongodb_connection_string

# Media Storage Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```



## System Execution Protocol

1. **Initialize Application:**
```bash
streamlit run app.py

```


2. **Authentication:** Access the local network URL provided in the terminal. Register an administrator account to initialize the `student_performance_db` database and `users` collection.
3. **Data Ingestion:** Navigate to **2_Data_Upload**. Upload a student dataset (`.csv` or `.xlsx`). The dataset must contain 15 columns, including `StudentID`.
4. **Risk Prediction:** Navigate to **3_Risk_Predictions** to execute the modular ensemble. The system achieves an **88.50% accuracy** rate. Results are automatically synchronized to the MongoDB `predictions` collection.
5. **Insights Verification:** Navigate to **4_Student_Insights** to analyze individual student variances against cohort averages using the Explainable AI (XAI) module.

## Data Schema Parameters

The serialized model utilizes a **Voting Classifier** trained on 14 predictive features:

* **Behavioral Pillar:** `StudyHours`, `Attendance`, `Discussions`, `OnlineCourses`
* **Psychological Pillar:** `Motivation`, `StressLevel`
* **Academic Pillar:** `AssignmentCompletion`, `Resources`, `EduTech`, `Internet`, `LearningStyle`, `Extracurricular`, `Age`, `Gender`

---

Would you like me to help you generate the **Appendix** section containing the specific code snippets for your report next?
