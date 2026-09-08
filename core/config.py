"""
Configuration module for ByteBreaker Framework
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import os
import json
from pathlib import Path


@dataclass
class ScannerConfig:
    """Scanner configuration settings"""
    timeout: int = 5
    max_threads: int = 50
    port_range: tuple = (1, 65535)
    aggressive_mode: bool = False
    stealth_mode: bool = True
    rate_limit: int = 10
    user_agent: str = "ByteBreaker/1.0"


@dataclass
class ExploitConfig:
    """Exploit module configuration"""
    safe_mode: bool = True
    max_payload_size: int = 1024
    allowed_targets: List[str] = field(default_factory=list)
    exploitation_timeout: int = 30
    verify_payloads: bool = True


@dataclass
class CrackConfig:
    """Hash cracking configuration"""
    hash_types: List[str] = field(default_factory=lambda: ["md5", "sha1", "sha256"])
    use_gpu: bool = False
    wordlist_path: Optional[str] = None
    rainbow_table_path: Optional[str] = None
    max_attempts: int = 1000000


@dataclass
class MLConfig:
    """Machine Learning configuration"""
    model_path: str = "models/threat_classifier.pkl"
    training_data_path: str = "data/training_data.csv"
    confidence_threshold: float = 0.85
    feature_columns: List[str] = field(default_factory=list)


class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.getenv("BYTEBREAKER_CONFIG", "config.json")
        self.scanner = ScannerConfig()
        self.exploit = ExploitConfig()
        self.cracker = CrackConfig()
        self.ml = MLConfig()
        
        self.data_dir = Path("data")
        self.reports_dir = Path("data/reports")
        self.logs_dir = Path("data/logs")
        self.wordlists_dir = Path("data/wordlists")
        self.models_dir = Path("models")
        
        self._load_config()
        self._create_directories()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Update scanner config
                if "scanner" in config_data:
                    for key, value in config_data["scanner"].items():
                        if hasattr(self.scanner, key):
                            setattr(self.scanner, key, value)
                
                # Update exploit config
                if "exploit" in config_data:
                    for key, value in config_data["exploit"].items():
                        if hasattr(self.exploit, key):
                            setattr(self.exploit, key, value)
                
                # Update cracker config
                if "cracker" in config_data:
                    for key, value in config_data["cracker"].items():
                        if hasattr(self.cracker, key):
                            setattr(self.cracker, key, value)
                
                # Update ML config
                if "ml" in config_data:
                    for key, value in config_data["ml"].items():
                        if hasattr(self.ml, key):
                            setattr(self.ml, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def _create_directories(self) -> None:
        """Create necessary directories"""
        for dir_path in [self.data_dir, self.reports_dir, self.logs_dir, 
                        self.wordlists_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        config_data = {
            "scanner": self.scanner.__dict__,
            "exploit": self.exploit.__dict__,
            "cracker": self.cracker.__dict__,
            "ml": self.ml.__dict__
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def validate_config(self) -> bool:
        """Validate configuration settings"""
        try:
            if self.scanner.max_threads < 1 or self.scanner.max_threads > 500:
                return False
            if self.scanner.port_range[0] > self.scanner.port_range[1]:
                return False
            if not self.cracker.hash_types:
                return False
            return True
        except Exception:
            return False
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "scanner": self.scanner.__dict__,
            "exploit": self.exploit.__dict__,
            "cracker": self.cracker.__dict__,
            "ml": self.ml.__dict__,
            "paths": {
                "data_dir": str(self.data_dir),
                "reports_dir": str(self.reports_dir),
                "logs_dir": str(self.logs_dir),
                "wordlists_dir": str(self.wordlists_dir),
                "models_dir": str(self.models_dir)
            }
        }
