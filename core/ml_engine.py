"""
ML Engine for ByteBreaker
"""
import numpy as np
from typing import Dict, Any, List
import json
from datetime import datetime

class MLEngine:
    """Machine Learning engine for threat analysis"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.threat_history = []
    
    def analyze_scan(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scan results for threats"""
        vulnerabilities = scan_results.get("vulnerabilities", [])
        
        # Calculate threat metrics
        critical = sum(1 for v in vulnerabilities if v.get("severity") == "critical")
        high = sum(1 for v in vulnerabilities if v.get("severity") == "high")
        medium = sum(1 for v in vulnerabilities if v.get("severity") == "medium")
        low = sum(1 for v in vulnerabilities if v.get("severity") == "low")
        
        # Calculate risk score
        risk_score = critical * 30 + high * 15 + medium * 5 + low * 1
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "CRITICAL"
        elif risk_score >= 40:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate recommendations
        recommendations = []
        if critical > 0:
            recommendations.append("Corrigir vulnerabilidades críticas imediatamente")
        if high > 0:
            recommendations.append("Implementar patches de segurança")
        if medium > 0:
            recommendations.append("Revisar configurações de segurança")
        
        analysis = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "vulnerability_counts": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat()
        }
        
        self.threat_history.append(analysis)
        return analysis
    
    def get_threat_trend(self) -> Dict[str, Any]:
        """Get threat trend over time"""
        if not self.threat_history:
            return {"trend": "No data"}
        
        scores = [t.get("risk_score", 0) for t in self.threat_history]
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        return {
            "average_score": avg_score,
            "max_score": max_score,
            "min_score": min_score,
            "total_analyses": len(scores),
            "trend": "increasing" if len(scores) > 1 and scores[-1] > scores[0] else "decreasing"
        }
