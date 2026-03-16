"""
Production-grade ML Training Pipeline for Healthcare Risk Prediction
Author: ML Engineer
Date: 2024
"""

import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel, RFECV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix,
    precision_recall_curve, average_precision_score
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Imbalanced learning
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline as ImbPipeline

# XGBoost for advanced modeling
import xgboost as xgb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HealthcareRiskPredictor:
    """
    Production-grade ML pipeline for healthcare risk prediction
    """
    
    def __init__(self, config=None):
        """
        Initialize the pipeline with configuration
        """
        self.config = config or self.get_default_config()
        self.model = None
        self.preprocessor = None
        self.feature_selector = None
        self.label_encoder = None
        self.scaler = None
        self.selected_features = None
        self.feature_importance = None
        self.training_metrics = {}
        
        # Create necessary directories
        Path("models").mkdir(exist_ok=True)
        Path("reports").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
    @staticmethod
    def get_default_config():
        """Default configuration for the pipeline"""
        return {
            'test_size': 0.2,
            'random_state': 42,
            'cv_folds': 5,
            'handle_imbalance': True,
            'imbalance_method': 'smote',  # 'smote', 'adasyn', 'smote_tomek'
            'feature_selection': True,
            'feature_selection_method': 'rfecv',  # 'rfecv', 'model_based'
            'model_type': 'xgboost',  # 'random_forest', 'gradient_boosting', 'xgboost', 'ensemble'
            'scaling': 'robust',  # 'standard', 'robust', 'minmax'
            'hyperparameter_tuning': True,
            'n_iter_search': 20,
            'threshold_tuning': True,
            'save_artifacts': True
        }
    
    def load_and_explore_data(self, filepath):
        """
        Load dataset and perform initial exploration
        """
        logger.info(f"Loading data from {filepath}")
        
        # Load dataset
        df = pd.read_csv(filepath)
        
        # Handle potential formatting issues
        if len(df.columns) == 1:
            logger.info("Fixing column formatting...")
            df = df[df.columns[0]].str.replace('"', '').str.split(",", expand=True)
            df.columns = [
                "id", "age", "gender", "bmi", "daily_steps", "sleep_hours", 
                "water_intake_l", "calories_consumed", "smoker", "alcohol",
                "resting_hr", "systolic_bp", "diastolic_bp", "cholesterol",
                "family_history", "disease_risk"
            ]
        
        # Data exploration
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Data types:\n{df.dtypes}")
        logger.info(f"Missing values:\n{df.isnull().sum()}")
        logger.info(f"Target distribution:\n{df['disease_risk'].value_counts()}")
        
        return df
    
    def clean_data(self, df):
        """
        Comprehensive data cleaning
        """
        logger.info("Starting data cleaning...")
        
        # Make a copy to avoid warnings
        df_clean = df.copy()
        
        # Define numeric columns (excluding id and target)
        numeric_cols = [
            "age", "bmi", "daily_steps", "sleep_hours", "water_intake_l",
            "calories_consumed", "smoker", "alcohol", "resting_hr",
            "systolic_bp", "diastolic_bp", "cholesterol", "family_history"
        ]
        
        # Convert to numeric, coercing errors to NaN
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Handle missing values
        logger.info("Handling missing values...")
        
        # For numerical columns, use median imputation
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                logger.info(f"Filled {df_clean[col].isnull().sum()} missing values in {col} with median: {median_val}")
        
        # Handle outliers using IQR method
        logger.info("Handling outliers...")
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
            if len(outliers) > 0:
                logger.info(f"Found {len(outliers)} outliers in {col}")
                # Cap outliers
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
        
        # Create derived features (domain knowledge)
        logger.info("Creating derived features...")
        df_clean['bmi_category'] = pd.cut(df_clean['bmi'], 
                                          bins=[0, 18.5, 25, 30, 100], 
                                          labels=['underweight', 'normal', 'overweight', 'obese'])
        
        df_clean['bp_category'] = pd.cut(df_clean['systolic_bp'],
                                         bins=[0, 120, 130, 140, 200],
                                         labels=['normal', 'elevated', 'high_stage1', 'high_stage2'])
        
        df_clean['age_group'] = pd.cut(df_clean['age'],
                                       bins=[0, 30, 45, 60, 100],
                                       labels=['young', 'middle', 'senior', 'elderly'])
        
        df_clean['health_score'] = (
            (df_clean['daily_steps'] / 10000) * 0.2 +
            (df_clean['sleep_hours'] / 8) * 0.2 +
            (1 - df_clean['bmi'] / 40) * 0.3 +
            (1 - df_clean['resting_hr'] / 100) * 0.3
        )
        
        # Encode categorical variables
        logger.info("Encoding categorical variables...")
        categorical_cols = ['gender', 'bmi_category', 'bp_category', 'age_group']
        
        for col in categorical_cols:
            if col in df_clean.columns:
                le = LabelEncoder()
                df_clean[col + '_encoded'] = le.fit_transform(df_clean[col].astype(str))
                # Save encoder for later use
                if col == 'gender':
                    self.label_encoder = le
        
        # Drop original categorical columns and id
        cols_to_drop = ['id', 'gender', 'bmi_category', 'bp_category', 'age_group']
        df_clean = df_clean.drop(columns=[col for col in cols_to_drop if col in df_clean.columns])
        
        logger.info(f"Data cleaning completed. Final shape: {df_clean.shape}")
        return df_clean
    
    def prepare_features_target(self, df, target_col='disease_risk'):
        """
        Prepare features and target variables
        """
        logger.info("Preparing features and target...")
        
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target distribution:\n{y.value_counts()}")
        
        return X, y
    
    def handle_class_imbalance(self, X, y):
        """
        Handle class imbalance using various techniques
        """
        if not self.config['handle_imbalance']:
            logger.info("Skipping imbalance handling as per config")
            return X, y
        
        logger.info(f"Handling class imbalance using {self.config['imbalance_method']}...")
        
        # Choose imbalance handling method
        if self.config['imbalance_method'] == 'smote':
            sampler = SMOTE(random_state=self.config['random_state'])
        elif self.config['imbalance_method'] == 'adasyn':
            sampler = ADASYN(random_state=self.config['random_state'])
        elif self.config['imbalance_method'] == 'smote_tomek':
            sampler = SMOTETomek(random_state=self.config['random_state'])
        else:
            logger.warning(f"Unknown imbalance method: {self.config['imbalance_method']}. Using SMOTE.")
            sampler = SMOTE(random_state=self.config['random_state'])
        
        # Apply sampling
        X_resampled, y_resampled = sampler.fit_resample(X, y)
        
        logger.info(f"Resampled data shape: {X_resampled.shape}")
        logger.info(f"New target distribution:\n{pd.Series(y_resampled).value_counts()}")
        
        return X_resampled, y_resampled
    
    def select_features(self, X, y):
        """
        Select most important features
        """
        if not self.config['feature_selection']:
            logger.info("Skipping feature selection as per config")
            return X, X.columns.tolist()
        
        logger.info(f"Performing feature selection using {self.config['feature_selection_method']}...")
        
        if self.config['feature_selection_method'] == 'rfecv':
            # Recursive Feature Elimination with Cross Validation
            estimator = RandomForestClassifier(n_estimators=100, random_state=self.config['random_state'])
            self.feature_selector = RFECV(
                estimator=estimator,
                step=1,
                cv=StratifiedKFold(self.config['cv_folds']),
                scoring='f1_weighted',
                n_jobs=-1
            )
            self.feature_selector.fit(X, y)
            
            selected_features = X.columns[self.feature_selector.support_].tolist()
            logger.info(f"RFECV selected {len(selected_features)} features")
            
        elif self.config['feature_selection_method'] == 'model_based':
            # Model-based feature selection
            model = RandomForestClassifier(n_estimators=100, random_state=self.config['random_state'])
            model.fit(X, y)
            
            # Get feature importance
            importance = pd.DataFrame({
                'feature': X.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Select features with cumulative importance > 95%
            importance['cumulative'] = importance['importance'].cumsum()
            selected_features = importance[importance['cumulative'] <= 0.95]['feature'].tolist()
            
            if len(selected_features) == 0:  # If all features are important
                selected_features = importance.head(max(1, len(X.columns) // 2))['feature'].tolist()
            
            logger.info(f"Model-based selection: {len(selected_features)} features")
            self.feature_importance = importance
        
        else:
            logger.warning(f"Unknown feature selection method. Using all features.")
            return X, X.columns.tolist()
        
        # Apply feature selection
        X_selected = X[selected_features]
        self.selected_features = selected_features
        
        logger.info(f"Selected features: {selected_features}")
        return X_selected, selected_features
    
    def scale_features(self, X_train, X_test):
        """
        Scale features using appropriate scaler
        """
        logger.info(f"Scaling features using {self.config['scaling']}...")
        
        if self.config['scaling'] == 'standard':
            self.scaler = StandardScaler()
        elif self.config['scaling'] == 'robust':
            self.scaler = RobustScaler()
        else:
            logger.warning(f"Unknown scaling method. Using RobustScaler.")
            self.scaler = RobustScaler()
        
        # Fit on training data and transform both
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame for interpretability
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
        
        return X_train_scaled, X_test_scaled
    
    def get_model(self):
        """
        Get the appropriate model based on configuration
        """
        logger.info(f"Initializing model: {self.config['model_type']}")
        
        if self.config['model_type'] == 'random_forest':
            model = RandomForestClassifier(
                n_estimators=300,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight='balanced',
                random_state=self.config['random_state'],
                n_jobs=-1
            )
        elif self.config['model_type'] == 'gradient_boosting':
            model = GradientBoostingClassifier(
                n_estimators=300,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                random_state=self.config['random_state']
            )
        elif self.config['model_type'] == 'xgboost':
            model = xgb.XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                objective='multi:softprob',
                random_state=self.config['random_state'],
                use_label_encoder=False,
                eval_metric='mlogloss'
            )
        elif self.config['model_type'] == 'ensemble':
            # Create a voting ensemble
            from sklearn.ensemble import VotingClassifier
            
            rf = RandomForestClassifier(n_estimators=200, random_state=self.config['random_state'])
            gb = GradientBoostingClassifier(n_estimators=200, random_state=self.config['random_state'])
            xgb_model = xgb.XGBClassifier(n_estimators=200, random_state=self.config['random_state'])
            
            model = VotingClassifier(
                estimators=[('rf', rf), ('gb', gb), ('xgb', xgb_model)],
                voting='soft',
                weights=[1, 1, 1]
            )
        else:
            logger.warning(f"Unknown model type. Using Random Forest.")
            model = RandomForestClassifier(
                n_estimators=200,
                class_weight='balanced',
                random_state=self.config['random_state']
            )
        
        return model
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train the model
        """
        logger.info("Starting model training...")
        
        # Get model
        self.model = self.get_model()
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Get feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            logger.info(f"Top 5 important features:\n{self.feature_importance.head()}")
        
        logger.info("Model training completed")
        return self.model
    
    def evaluate(self, model, X_test, y_test):
        """
        Comprehensive model evaluation
        """
        logger.info("Performing comprehensive model evaluation...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_macro': precision_score(y_test, y_pred, average='macro'),
            'recall_macro': recall_score(y_test, y_pred, average='macro'),
            'f1_macro': f1_score(y_test, y_pred, average='macro'),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted'),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
        }
        
        # Calculate ROC AUC for multiclass
        try:
            metrics['roc_auc_ovr'] = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
            metrics['roc_auc_ovo'] = roc_auc_score(y_test, y_pred_proba, multi_class='ovo')
        except Exception as e:
            logger.warning(f"Could not calculate ROC AUC: {e}")
        
        # Log metrics
        logger.info("Evaluation Metrics:")
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value:.4f}")
        
        # Generate classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        metrics['classification_report'] = report
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        self.training_metrics = metrics
        return metrics
    
    def cross_validate(self, model, X, y):
        """
        Perform cross-validation
        """
        logger.info(f"Performing {self.config['cv_folds']}-fold cross-validation...")
        
        cv = StratifiedKFold(n_splits=self.config['cv_folds'], shuffle=True, 
                            random_state=self.config['random_state'])
        
        # Perform cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted', n_jobs=-1)
        
        logger.info(f"Cross-validation F1 scores: {cv_scores}")
        logger.info(f"CV F1 Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return cv_scores
    
    def find_optimal_threshold(self, model, X_val, y_val):
        """
        Find optimal threshold for each class
        """
        if not self.config['threshold_tuning']:
            logger.info("Skipping threshold tuning")
            return None
        
        logger.info("Finding optimal thresholds for each class...")
        
        # Get prediction probabilities
        y_proba = model.predict_proba(X_val)
        
        # For each class, find optimal threshold
        classes = model.classes_
        optimal_thresholds = {}
        
        for i, class_label in enumerate(classes):
            # Convert to binary problem
            y_binary = (y_val == class_label).astype(int)
            class_proba = y_proba[:, i]
            
            # Calculate precision-recall curve
            precision, recall, thresholds = precision_recall_curve(y_binary, class_proba)
            
            # Find threshold that maximizes F1 score
            f1_scores = 2 * (precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1] + 1e-10)
            best_idx = np.argmax(f1_scores)
            best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
            
            optimal_thresholds[class_label] = best_threshold
            logger.info(f"Class {class_label}: Optimal threshold = {best_threshold:.4f}")
        
        return optimal_thresholds
    
    def save_artifacts(self, model, metrics, feature_names):
        """
        Save all model artifacts for production
        """
        if not self.config['save_artifacts']:
            logger.info("Skipping artifact saving as per config")
            return
        
        logger.info("Saving model artifacts...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save model
        model_path = f"models/healthcare_model_{timestamp}.pkl"
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler
        scaler_path = f"models/scaler_{timestamp}.pkl"
        joblib.dump(self.scaler, scaler_path)
        
        # Save feature selector if exists
        if self.feature_selector:
            selector_path = f"models/feature_selector_{timestamp}.pkl"
            joblib.dump(self.feature_selector, selector_path)
        
        # Save label encoder
        encoder_path = f"models/label_encoder_{timestamp}.pkl"
        joblib.dump(self.label_encoder, encoder_path)
        
        # Save selected features list
        features_path = f"models/selected_features_{timestamp}.json"
        with open(features_path, 'w') as f:
            json.dump({
                'selected_features': feature_names,
                'model_type': self.config['model_type'],
                'metrics': {k: v for k, v in metrics.items() if isinstance(v, (int, float, str))}
            }, f, indent=4)
        
        # Save configuration
        config_path = f"models/config_{timestamp}.json"
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        # Save feature importance if available
        if self.feature_importance is not None:
            importance_path = f"models/feature_importance_{timestamp}.csv"
            self.feature_importance.to_csv(importance_path, index=False)
        
        # Create a production-ready model package
        production_model = {
            'model': model,
            'scaler': self.scaler,
            'feature_selector': self.feature_selector,
            'label_encoder': self.label_encoder,
            'selected_features': feature_names,
            'config': self.config,
            'metrics': metrics
        }
        
        production_path = f"models/production_model_{timestamp}.pkl"
        joblib.dump(production_model, production_path)
        logger.info(f"Production-ready model package saved to {production_path}")
        
        return {
            'model_path': model_path,
            'production_path': production_path,
            'timestamp': timestamp
        }
    
    def run_pipeline(self, data_path):
        """
        Run the complete training pipeline
        """
        logger.info("="*50)
        logger.info("Starting Healthcare Risk Prediction Pipeline")
        logger.info("="*50)
        
        try:
            # Step 1: Load and explore data
            df = self.load_and_explore_data(data_path)
            
            # Step 2: Clean data
            df_clean = self.clean_data(df)
            
            # Step 3: Prepare features and target
            X, y = self.prepare_features_target(df_clean)
            
            # Step 4: Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=self.config['test_size'],
                random_state=self.config['random_state'],
                stratify=y  # Maintain class distribution
            )
            
            # Step 5: Handle class imbalance (apply only to training data)
            if self.config['handle_imbalance']:
                X_train_balanced, y_train_balanced = self.handle_class_imbalance(X_train, y_train)
            else:
                X_train_balanced, y_train_balanced = X_train, y_train
            
            # Step 6: Feature selection
            if self.config['feature_selection']:
                X_train_selected, selected_features = self.select_features(X_train_balanced, y_train_balanced)
                X_test_selected = X_test[selected_features]
            else:
                X_train_selected = X_train_balanced
                X_test_selected = X_test
                selected_features = X.columns.tolist()
            
            # Step 7: Scale features
            X_train_scaled, X_test_scaled = self.scale_features(X_train_selected, X_test_selected)
            
            # Step 8: Further split for validation
            X_train_final, X_val, y_train_final, y_val = train_test_split(
                X_train_scaled, y_train_balanced,
                test_size=0.2,
                random_state=self.config['random_state'],
                stratify=y_train_balanced
            )
            
            # Step 9: Train model
            model = self.train(X_train_final, y_train_final, X_val, y_val)
            
            # Step 10: Evaluate model
            metrics = self.evaluate(model, X_test_scaled, y_test)
            
            # Step 11: Cross-validation
            cv_scores = self.cross_validate(model, X_train_scaled, y_train_balanced)
            metrics['cv_mean'] = cv_scores.mean()
            metrics['cv_std'] = cv_scores.std()
            
            # Step 12: Find optimal thresholds (optional)
            thresholds = self.find_optimal_threshold(model, X_val, y_val)
            metrics['optimal_thresholds'] = thresholds
            
            # Step 13: Save artifacts
            artifacts = self.save_artifacts(model, metrics, selected_features)
            
            logger.info("="*50)
            logger.info("Pipeline completed successfully!")
            logger.info(f"Final Model Performance:")
            logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
            logger.info(f"F1 Score (weighted): {metrics['f1_weighted']:.4f}")
            logger.info(f"Cross-validation F1: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']*2:.4f})")
            logger.info("="*50)
            
            return {
                'model': model,
                'metrics': metrics,
                'artifacts': artifacts,
                'selected_features': selected_features
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise


def create_prediction_api(model_package_path):
    """
    Create a simple prediction API function
    """
    # Load the production model package
    production_model = joblib.load(model_package_path)
    
    def predict(features_dict):
        """
        Make predictions on new data
        """
        # Convert features to DataFrame
        df = pd.DataFrame([features_dict])
        
        # Apply same preprocessing as training
        # Note: You'll need to implement the same preprocessing steps here
        # This is a simplified version
        
        # Select features
        X = df[production_model['selected_features']]
        
        # Scale features
        X_scaled = production_model['scaler'].transform(X)
        
        # Make prediction
        prediction = production_model['model'].predict(X_scaled)
        probabilities = production_model['model'].predict_proba(X_scaled)
        
        # Decode prediction if needed
        if production_model['label_encoder']:
            prediction = production_model['label_encoder'].inverse_transform(prediction)
        
        return {
            'prediction': prediction.tolist(),
            'probabilities': probabilities.tolist(),
            'risk_level': prediction[0]  # Assuming single prediction
        }
    
    return predict


if __name__ == "__main__":
    # Configuration - You can modify these based on your needs
    config = {
        'test_size': 0.2,
        'random_state': 42,
        'cv_folds': 5,
        'handle_imbalance': True,
        'imbalance_method': 'smote',  # Options: 'smote', 'adasyn', 'smote_tomek'
        'feature_selection': True,
        'feature_selection_method': 'rfecv',  # Options: 'rfecv', 'model_based'
        'model_type': 'xgboost',  # Options: 'random_forest', 'gradient_boosting', 'xgboost', 'ensemble'
        'scaling': 'robust',  # Options: 'standard', 'robust', 'minmax'
        'threshold_tuning': True,
        'save_artifacts': True
    }
    
    # Initialize pipeline
    pipeline = HealthcareRiskPredictor(config)
    
    # Run pipeline
    data_path = "dataset/health_lifestyle_dataset.csv"  # Update this path
    results = pipeline.run_pipeline(data_path)
    
    # Example: Create prediction function for the best model
    if results and 'artifacts' in results:
        predict_function = create_prediction_api(results['artifacts']['production_path'])
        
        # Example prediction
        sample_patient = {
            'age': 45,
            'bmi': 27.5,
            'daily_steps': 7500,
            'sleep_hours': 7,
            'water_intake_l': 2.5,
            'calories_consumed': 2200,
            'smoker': 0,
            'alcohol': 1,
            'resting_hr': 72,
            'systolic_bp': 125,
            'diastolic_bp': 82,
            'cholesterol': 190,
            'family_history': 0,
            'gender_encoded': 0,
            'bmi_category_encoded': 2,
            'bp_category_encoded': 1,
            'age_group_encoded': 2,
            'health_score': 0.65
        }
        
        # Make prediction
        prediction = predict_function(sample_patient)
        print(f"\nSample Prediction: {prediction}")