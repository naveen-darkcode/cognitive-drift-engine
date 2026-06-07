# Cognitive Drift Engine

A machine learning system that detects cognitive fatigue using behavioral biometrics and user interaction patterns.

## Overview

The Cognitive Drift Engine monitors user behavior during computer usage and predicts cognitive fatigue levels based on:

* Keystroke dynamics
* Typing speed
* Dwell time
* Mouse activity
* Click frequency
* Application switching behavior

The system classifies fatigue into three levels:

* LOW
* MEDIUM
* HIGH

---

## Features

### Keyboard Features

* Inter-Key Interval (IKI) Variance
* Backspace Ratio
* Dwell Time
* Typing Speed

### Behavioral Features

* Mouse Activity
* Click Count
* App Switch Rate

---

## Machine Learning Model

Final Model:

* Extra Trees Classifier
* 200 Trees
* Balanced Class Weights

Training Dataset:

Training Dataset:

- 51 Real User Sessions
- 211 Behavioral Feature Windows

Fatigue Classes:

- LOW
- MEDIUM
- HIGH

Final Model:

- Extra Trees Classifier
- 200 Trees
- Balanced Class Weights
---

## Project Structure

database/
models/
preprocessing/
tracking/

requirements.txt
README.md

---

## Installation

pip install -r requirements.txt

---

## Train Final Model

python models/train_final.py

---

## Predict Fatigue

python models/predict_fatigue.py

Example Output:

{
"fatigue_level": "MEDIUM",
"confidence": 95.0
}

---

## Authors

Cognitive Drift Engine Project Team

## Model Performance

Model Comparison:

- Random Forest: 60.47%
- Extra Trees: 67.44%
- Gradient Boosting: 65.12%

Best Model:

- Extra Trees Classifier

Classification Results:

HIGH:
- Precision: 0.75
- Recall: 0.56
- F1 Score: 0.64

LOW:
- Precision: 0.75
- Recall: 0.30
- F1 Score: 0.43

MEDIUM:
- Precision: 0.63
- Recall: 1.00
- F1 Score: 0.77

Overall Accuracy:
67.44%