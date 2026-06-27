
https://www.kaggle.com/mlg-ulb/creditcardfraud
👆dataset used.
# Overview
- Detect fraudulent transactions in financial data using advanced analytics and machine learning. This project focuses on identifying suspicious patterns and anomalies in large-scale transaction datasets.

# Objectives
- Minimize revenue loss due to fraud by implementing robust detection systems. 
- Create models that can distinguish between legitimate and fraudulent transactions with high accuracy.

# Methodology
- Outlier analysis techniques
- Anomaly detection algorithms
- Autoencoder Neural Networks implementation
- Feature engineering for fraud indicators
- Imbalanced data handling techniques

# Progress
- [x] Data Acquisition and Understanding: Loaded and explored the creditcard.csv dataset. Confirmed structure: 31 columns (Time, V1-V28, Amount, Class), ~284k transactions, highly imbalanced (fraud rate ~0.17%). No missing values.
- [x] Exploratory Data Analysis: Created visualizations for class distribution, amount and time distributions, correlation heatmap. Saved plots as PNG files.
- [x] Data Preprocessing: Handled imbalanced data with SMOTE, created time-based features (Hour, Day), scaled Amount.
- [x] Feature Engineering: Added Hour and Day features from Time column.
- [x] Modeling: Implemented Autoencoder for anomaly detection and Isolation Forest for outlier analysis.
- [x] Evaluation: Evaluated models with classification reports, ROC AUC, confusion matrices. Autoencoder achieved 0.906 ROC AUC (precision 0.95, recall 0.86 on fraud). Isolation Forest achieved 0.883 ROC AUC (precision 0.90, recall 0.87 on fraud).
- [x] Deployment: Created reproducible script, requirements.txt, and README.md for the project.