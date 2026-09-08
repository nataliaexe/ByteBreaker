"""
ML Threat Detector Module
"""
import numpy as np
from typing import Dict, Any, List
import json
from datetime import datetime

class MLDetector:
    """Machine Learning based threat detection"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.model = None
        self.threat_patterns = []
    
    def extract_features(self, scan_results: Dict[str, Any]) -> np.ndarray:
        """Extract features from scan results"""
        features = []
        
        # Network features
        open_ports = scan_results.get("open_ports", [])
        features.append(len(open_ports))
        
        # Vulnerability features
        vulnerabilities = scan_results.get("vulnerabilities", [])
        features.append(len(vulnerabilities))
        features.append(sum(1 for v in vulnerabilities if v.get("severity") == "critical"))
        features.append(sum(1 for v in vulnerabilities if v.get("severity") == "high"))
        
        # Web features
        features.append(1 if any(p.get("port") in [80, 443, 8080] for p in open_ports) else 0)
        features.append(1 if any(p.get("port") in [3306, 5432] for p in open_ports) else 0)
        
        return np.array(features).reshape(1, -1)
    
    def analyze_threat_level(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze threat level based on scan results"""
        threat_score = 0
        threat_factors = []
        
        # Count vulnerabilities by severity
        vulnerabilities = scan_results.get("vulnerabilities", [])
        critical = sum(1 for v in vulnerabilities if v.get("severity") == "critical")
        high = sum(1 for v in vulnerabilities if v.get("severity") == "high")
        medium = sum(1 for v in vulnerabilities if v.get("severity") == "medium")
        
        # Calculate threat score (0-100)
        threat_score += critical * 30
        threat_score += high * 15
        threat_score += medium * 5
        
        if critical > 0:
            threat_factors.append(f"{critical} vulnerabilidades críticas")
        if high > 0:
            threat_factors.append(f"{high} vulnerabilidades altas")
        if medium > 0:
            threat_factors.append(f"{medium} vulnerabilidades médias")
        
        # Cap at 100
        threat_score = min(threat_score, 100)
        
        # Determine threat level
        if threat_score >= 70:
            threat_level = "CRITICAL"
        elif threat_score >= 40:
            threat_level = "HIGH"
        elif threat_score >= 20:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        return {
            "threat_score": threat_score,
            "threat_level": threat_level,
            "threat_factors": threat_factors,
            "analyzed_at": datetime.now().isoformat()
        }
