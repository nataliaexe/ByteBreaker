"""
Machine Learning utilities for ByteBreaker
"""
import pickle
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np


class ThreatClassifier:
    """Machine learning model for threat classification"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "models/threat_classifier.pkl"
        self.model = None
        self.feature_names = []
        
        if Path(self.model_path).exists():
            self.load_model()
    
    def load_model(self) -> bool:
        """Load ML model from file"""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data.get("model")
                self.feature_names = model_data.get("feature_names", [])
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def save_model(self) -> bool:
        """Save ML model to file"""
        if not self.model:
            return False
        
        try:
            Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
            model_data = {
                "model": self.model,
                "feature_names": self.feature_names
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def train(self, X: np.ndarray, y: np.ndarray, 
              feature_names: Optional[List[str]] = None) -> bool:
        """Train ML model"""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X_train, y_train)
            
            # Store feature names
            if feature_names:
                self.feature_names = feature_names
            
            # Save model
            self.save_model()
            
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, X: np.ndarray) -> List[int]:
        """Make predictions using ML model"""
        if not self.model:
            raise ValueError("Model not loaded or trained")
        
        try:
            return self.model.predict(X).tolist()
        except Exception as e:
            print(f"Error making predictions: {e}")
            return []
    
    def predict_proba(self, X: np.ndarray) -> List[List[float]]:
        """Get prediction probabilities"""
        if not self.model:
            raise ValueError("Model not loaded or trained")
        
        try:
            return self.model.predict_proba(X).tolist()
        except Exception as e:
            print(f"Error getting probabilities: {e}")
            return []
    
    def classify_threat(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Classify if features indicate a threat"""
        if not self.model or not self.feature_names:
            return {"error": "Model not loaded"}
        
        try:
            # Convert features to array in correct order
            feature_vector = []
            for feature_name in self.feature_names:
                feature_vector.append(features.get(feature_name, 0))
            
            X = np.array([feature_vector])
            prediction = self.predict(X)[0]
            probability = self.predict_proba(X)[0] if hasattr(self.model, 'predict_proba') else []
            
            return {
                "prediction": prediction,
                "probability": max(probability) if probability else 0,
                "is_threat": prediction == 1,
                "confidence": max(probability) if probability else 0
            }
        except Exception as e:
            return {"error": str(e)}
    
    def extract_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from data for ML model"""
        features = {}
        
        # Network-related features
        features["port_count"] = len(data.get("open_ports", []))
        features["has_web_server"] = any(
            port.get("port") in [80, 443, 8080, 8443] 
            for port in data.get("open_ports", [])
        )
        features["has_database"] = any(
            port.get("port") in [3306, 5432, 1433, 1521] 
            for port in data.get("open_ports", [])
        )
        
        # Vulnerability-related features
        vulnerabilities = data.get("vulnerabilities", [])
        features["vuln_count"] = len(vulnerabilities)
        features["critical_vulns"] = sum(
            1 for vuln in vulnerabilities if vuln.get("severity") == "critical"
        )
        features["high_vulns"] = sum(
            1 for vuln in vulnerabilities if vuln.get("severity") == "high"
        )
        
        # Web-related features
        features["has_ssl"] = data.get("ssl", {}).get("error") is None
        features["missing_headers"] = sum(
            1 for vuln in vulnerabilities 
            if vuln.get("type") == "missing_header"
        )
        
        return features
