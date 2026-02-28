import joblib
import pandas as pd
import os

# Load the saved model
script_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(script_dir, 'student_model.pkl'))

# Create data for ONE new student (No ExamScore needed!)
# These values should match your Excel column names
new_student = pd.DataFrame([{
    'StudyHours': 5,
    'Attendance': 60,
    'Resources': 0,
    'Extracurricular': 0,
    'Motivation': 0,
    'Internet': 1,
    'Gender': 1,
    'Age': 20,
    'LearningStyle': 1,
    'OnlineCourses': 2,
    'Discussions': 0,
    'AssignmentCompletion': 55,
    'EduTech': 0,
    'StressLevel': 2
}])

# Make the prediction
prediction = model.predict(new_student)[0]

# Human-friendly output
risk_map = {0: "Excellent", 1: "Good", 2: "Average", 3: "HIGH RISK / FAIL"}
print(f"Predicted Performance Level: {risk_map[prediction]}")