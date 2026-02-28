# Student Performance Prediction System

## System Overview

The Student Performance Prediction System is a machine learning-based early warning application. It utilizes a Modular Ensemble architecture (Voting Classifier) integrating Behavioral, Psychological, and Academic pillars to classify student risk levels. The presentation layer is constructed using Streamlit, with session state management and data persistence handled via MongoDB.

## Architecture & Technology Stack

* **Frontend/Interface:** Streamlit (Multipage Application)
* **Machine Learning:** Scikit-learn (Random Forest Classifier, Voting Classifier, Pipeline)
* **Data Manipulation:** Pandas
* **Model Serialization:** Joblib
* **Database:** MongoDB (Local or Atlas via `pymongo`)
* **Environment Management:** `python-dotenv`

## Project Directory Structure

```text
/ (Project Root Directory)
│
├── app.py                  # Main Streamlit application and Authentication Gateway
├── requirements.txt        # System dependencies
├── .env                    # Environment variables (MongoDB URI)
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
    │   └── student_model.pkl   # Serialized Voting Classifier model
    └── /scripts
        └── model_train.py      # Algorithm training script

```

## Prerequisites

1. Python 3.8 or higher installed on the execution environment.
2. Active MongoDB instance (Local port 27017 or MongoDB Atlas cloud cluster).

## Installation Protocol

1. **Clone the repository:**

```bash
git clone <repository_url>
cd student_performance_system

```

2. **Configure Environment Variables:**
Create a `.env` file in the root directory and insert the MongoDB connection string:

```text
MONGO_URI="mongodb+srv://<username>:<password>@<clustername>.mongodb.net/?retryWrites=true&w=majority"

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

2. **Authentication:** Access the local network URL provided in the terminal. Register a new administrator account to initialize the `student_performance_db` database and `users` collection.
3. **Data Ingestion:** Navigate to the Data Upload module. Upload the student dataset (`.csv` or `.xlsx`). The dataset must contain 15 columns, with `StudentID` acting as the primary identifier.
4. **Risk Prediction:** Navigate to the Risk Predictions module to execute the modular ensemble inference. The system drops the identifier and target variables prior to inference. Results are automatically synchronized to the MongoDB `predictions` collection.
5. **Insights Verification:** Navigate to the Student Insights module to analyze individual student variances against cohort averages.

## Data Schema Parameters

The serialized model requires the following 14 features for inference, processed via distinct pipelines:

* **Behavioral Pillar:** `StudyHours`, `Attendance`, `Discussions`, `OnlineCourses`
* **Psychological Pillar:** `Motivation`, `StressLevel`
* **Academic Pillar:** `AssignmentCompletion`, `Resources`, `EduTech`, `Internet`, `LearningStyle`, `Extracurricular`, `Age`, `Gender`