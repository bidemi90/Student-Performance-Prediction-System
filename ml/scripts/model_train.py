import pandas as pd
import os
import joblib  # This is the tool that "saves" the brain
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score

# 1. PATH SETUP
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'student_performance.xlsx')

# 2. LOAD DATA
try:
    df = pd.read_excel(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error: {e}")
    exit()

# 3. SETUP
target = 'FinalGrade'
X = df.drop(columns=[target])
y = df[target]

behavioral_cols = ['StudyHours', 'Attendance', 'Discussions', 'OnlineCourses']
psychological_cols = ['Motivation', 'StressLevel']
academic_cols = ['AssignmentCompletion', 'Resources', 'EduTech', 'Internet', 'LearningStyle', 'Extracurricular', 'Age', 'Gender']

# 4. SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. DEFINE 3-PILLAR MODELS
pipe_behavioral = Pipeline([
    ('selector', ColumnTransformer([('sel', 'passthrough', behavioral_cols)], remainder='drop')),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipe_psychological = Pipeline([
    ('selector', ColumnTransformer([('sel', 'passthrough', psychological_cols)], remainder='drop')),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipe_academic = Pipeline([
    ('selector', ColumnTransformer([('sel', 'passthrough', academic_cols)], remainder='drop')),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 6. ENSEMBLE
early_warning_system = VotingClassifier(
    estimators=[
        ('behavioral', pipe_behavioral),
        ('psychological', pipe_psychological),
        ('academic', pipe_academic)
    ],
    voting='soft'
)

# 7. TRAIN
print("Training and saving the modular system...")
early_warning_system.fit(X_train, y_train)

# 8. SAVE THE BRAIN
# This creates a file named 'student_model.pkl' in your scripts folder
model_save_path = os.path.join(script_dir, '../models/student_model.pkl')
joblib.dump(early_warning_system, model_save_path)

print(f"\n==========================================")
print(f"SUCCESS: Model saved at {model_save_path}")
print(f"Accuracy: {accuracy_score(y_test, early_warning_system.predict(X_test))*100:.2f}%")
print(f"==========================================")
