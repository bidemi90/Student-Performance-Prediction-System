
# Student Performance Prediction – Machine Learning Module

This module implements the machine learning component of the **Intelligent Student Performance Prediction System**.

The model is designed to classify students into **Low**, **Medium**, or **High** academic risk categories based on performance indicators.

---

## Features Used
- Attendance Rate
- Test Score
- Assignment Score
- Continuous Assessment
- Final Score

---

## Model Type
- Supervised Learning (Classification)
- Algorithm: Logistic Regression
- Labels: Low, Medium, High

---

## Dataset
- Format: Excel (.xlsx)
- Generated synthetically using Microsoft Excel
- Size: 100 student records
- Label generation based on rule-based grading thresholds

---

## Folder Structure
```

ml/
├── data/
│   └── student_training_data.xlsx
├── models/
│   ├── risk_model.pkl
│   └── label_encoder.pkl
├── scripts/
│   ├── train_model.py
│   └── predict.py

````

---

## Training the Model
```bash
python scripts/train_model.py
````

---

## Running Predictions

```bash
echo [{"attendance_rate":75,"test_score":68,"assignment_score":70,"continuous_assessment":72,"final_score":70}] | python scripts/predict.py
```

---

## Output

The model returns predicted academic risk levels for each student record.

```
Low | Medium | High
```

---

## Notes

* Input features must be on a consistent numerical scale.
* This module is integrated with a Node.js backend for system-level predictions.

````

---

## `ml/requirements.txt`

```txt
pandas
numpy
scikit-learn
joblib
openpyxl
````

---

