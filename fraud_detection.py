# Fraud Detection Project
# Based on data-science-analyst skill templates

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.ensemble import IsolationForest
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudDetector:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
    
    def load_data(self):
        logger.info("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Dataset shape: {self.df.shape}")
        logger.info(f"Columns: {self.df.columns.tolist()}")
        logger.info(f"Class distribution:\n{self.df['Class'].value_counts()}")
        logger.info(f"Missing values:\n{self.df.isnull().sum()}")
        return self.df
    
    def preprocess_data(self):
        logger.info("Preprocessing data...")
        # Feature engineering: Time-based features
        self.df['Hour'] = self.df['Time'] % (24 * 3600) // 3600
        self.df['Day'] = self.df['Time'] // (24 * 3600)
        
        # Scale Amount
        self.df['Amount_scaled'] = self.scaler.fit_transform(self.df[['Amount']])
        
        # Features for modeling
        features = [col for col in self.df.columns if col not in ['Time', 'Class', 'Amount']]
        X = self.df[features]
        y = self.df['Class']
        
        # Handle imbalance with SMOTE
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        logger.info(f"After SMOTE: {X_resampled.shape}, class distribution: {np.bincount(y_resampled)}")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
        )
        logger.info(f"Train shape: {self.X_train.shape}, Test shape: {self.X_test.shape}")
    
    def build_autoencoder(self):
        logger.info("Building autoencoder...")
        input_dim = self.X_train.shape[1]
        encoding_dim = 14  # bottleneck
        
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(encoding_dim, activation='relu')(input_layer)
        decoded = Dense(input_dim, activation='sigmoid')(encoded)
        
        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')
        
        # Train on normal transactions only
        X_normal = self.df[self.df['Class'] == 0].drop(['Time', 'Class', 'Amount'], axis=1)
        X_normal_scaled = self.scaler.fit_transform(X_normal)
        
        autoencoder.fit(X_normal_scaled, X_normal_scaled, epochs=50, batch_size=256, validation_split=0.2, verbose=0)
        
        self.models['autoencoder'] = autoencoder
        logger.info("Autoencoder trained.")
    
    def detect_anomalies_autoencoder(self, threshold=0.01):
        logger.info("Detecting anomalies with autoencoder...")
        X_test_scaled = self.scaler.transform(self.X_test)
        reconstructions = self.models['autoencoder'].predict(X_test_scaled)
        mse = np.mean(np.power(X_test_scaled - reconstructions, 2), axis=1)
        
        # Anomalies are high MSE
        predictions = (mse > threshold).astype(int)
        return predictions, mse
    
    def build_isolation_forest(self):
        logger.info("Building Isolation Forest...")
        # Use original imbalanced data for unsupervised anomaly detection
        X = self.df.drop(['Time', 'Class', 'Amount'], axis=1)
        y = self.df['Class']
        
        iso_forest = IsolationForest(contamination=0.0017, random_state=42)  # approx fraud rate
        iso_forest.fit(X)
        
        self.models['isolation_forest'] = iso_forest
        logger.info("Isolation Forest trained.")
    
    def detect_anomalies_isolation_forest(self):
        X_test_original = self.df.loc[self.X_test.index].drop(['Time', 'Class', 'Amount'], axis=1)
        predictions = self.models['isolation_forest'].predict(X_test_original)
        # IsolationForest: -1 for anomaly, 1 for normal
        predictions = (predictions == -1).astype(int)
        return predictions
    
    def evaluate_model(self, predictions, model_name):
        logger.info(f"Evaluating {model_name}...")
        print(f"\n{model_name} Results:")
        print(classification_report(self.y_test, predictions))
        print(f"ROC AUC: {roc_auc_score(self.y_test, predictions)}")
        
        cm = confusion_matrix(self.y_test, predictions)
        plt.figure(figsize=(6,4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'{model_name} Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'financial-fraud-detection/{model_name}_confusion_matrix.png')
        plt.show()
    
    def exploratory_data_analysis(self):
        logger.info("Performing EDA...")
        
        # Class distribution
        plt.figure(figsize=(6,4))
        sns.countplot(x='Class', data=self.df)
        plt.title('Class Distribution')
        plt.savefig('financial-fraud-detection/class_distribution.png')
        plt.show()
        
        # Amount distribution
        plt.figure(figsize=(10,6))
        sns.histplot(data=self.df, x='Amount', hue='Class', bins=50, alpha=0.7)
        plt.title('Transaction Amount Distribution by Class')
        plt.xlim(0, 500)  # Focus on lower amounts
        plt.savefig('financial-fraud-detection/amount_distribution.png')
        plt.show()
        
        # Time distribution
        plt.figure(figsize=(10,6))
        sns.histplot(data=self.df, x='Time', hue='Class', bins=50, alpha=0.7)
        plt.title('Transaction Time Distribution by Class')
        plt.savefig('financial-fraud-detection/time_distribution.png')
        plt.show()
        
        # Correlation heatmap for V1-V10
        plt.figure(figsize=(12,8))
        corr = self.df[['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','Amount','Class']].corr()
        sns.heatmap(corr, annot=False, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.savefig('financial-fraud-detection/correlation_heatmap.png')
        plt.show()
        
        logger.info("EDA completed. Plots saved.")

    def run_full_pipeline(self):
        self.load_data()
        self.exploratory_data_analysis()
        self.preprocess_data()
        self.build_autoencoder()
        self.build_isolation_forest()
        
        # Evaluate autoencoder
        ae_predictions, _ = self.detect_anomalies_autoencoder()
        self.evaluate_model(ae_predictions, 'Autoencoder')
        
        # Evaluate Isolation Forest
        if_predictions = self.detect_anomalies_isolation_forest()
        self.evaluate_model(if_predictions, 'Isolation Forest')

if __name__ == "__main__":
    detector = FraudDetector('creditcard.csv')
    detector.run_full_pipeline()