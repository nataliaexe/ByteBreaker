"""
Authorization and scope validation module
"""
from typing import List, Optional, Dict, Any
import ipaddress
from datetime import datetime, timedelta
import json
from pathlib import Path


class AuthorizationManager:
    """Manages authorization for testing targets"""
    
    def __init__(self, authorization_file: str = "authorizations.json"):
        self.authorization_file = Path(authorization_file)
        self.authorizations = self._load_authorizations()
    
    def _load_authorizations(self) -> Dict[str, Any]:
        """Load authorization records"""
        if self.authorization_file.exists():
            try:
                with open(self.authorization_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading authorizations: {e}")
                return {"targets": [], "history": []}
        return {"targets": [], "history": []}
    
    def save_authorizations(self) -> None:
        """Save authorization records"""
        try:
            with open(self.authorization_file, 'w') as f:
                json.dump(self.authorizations, f, indent=4)
        except Exception as e:
            print(f"Error saving authorizations: {e}")
    
    def add_authorization(self, target: str, scope: List[str], 
                         authorized_by: str, expires_in_days: int = 30) -> bool:
        """Add new authorization for target"""
        try:
            # Validate IP or domain
            if not self._is_valid_target(target):
                raise ValueError(f"Invalid target: {target}")
            
            # Check for existing authorization
            for auth in self.authorizations["targets"]:
                if auth["target"] == target and auth["status"] == "active":
                    print(f"Authorization already exists for {target}")
                    return False
            
            authorization = {
                "target": target,
                "scope": scope,
                "authorized_by": authorized_by,
                "authorized_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=expires_in_days)).isoformat(),
                "status": "active"
            }
            
            self.authorizations["targets"].append(authorization)
            self.save_authorizations()
            print(f"Authorization added for {target}")
            return True
            
        except Exception as e:
            print(f"Error adding authorization: {e}")
            return False
    
    def check_authorization(self, target: str, action: Optional[str] = None) -> bool:
        """Check if target is authorized for testing"""
        for auth in self.authorizations["targets"]:
            if auth["target"] == target and auth["status"] == "active":
                # Check expiration
                try:
                    expires_at = datetime.fromisoformat(auth["expires_at"])
                    if datetime.now() < expires_at:
                        # Check if action is in scope
                        if action and action not in auth["scope"]:
                            return False
                        return True
                except Exception:
                    continue
        return False
    
    def log_action(self, target: str, action: str, result: str) -> None:
        """Log testing action for audit purposes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "action": action,
            "result": result
        }
        self.authorizations["history"].append(log_entry)
        self.save_authorizations()
    
    def _is_valid_target(self, target: str) -> bool:
        """Validate target IP or domain"""
        try:
            # Check if IP address
            ipaddress.ip_address(target)
            return True
        except ValueError:
            # Check if domain
            if "." in target and not target.startswith(".") and not target.endswith("."):
                return True
        return False
    
    def list_authorizations(self) -> List[Dict[str, Any]]:
        """List all active authorizations"""
        return [auth for auth in self.authorizations["targets"] 
                if auth["status"] == "active"]
    
    def list_all_authorizations(self) -> List[Dict[str, Any]]:
        """List all authorizations including revoked/expired"""
        return self.authorizations["targets"]
    
    def revoke_authorization(self, target: str) -> bool:
        """Revoke authorization for target"""
        for auth in self.authorizations["targets"]:
            if auth["target"] == target and auth["status"] == "active":
                auth["status"] = "revoked"
                auth["revoked_at"] = datetime.now().isoformat()
                self.save_authorizations()
                return True
        return False
    
    def get_authorization_history(self) -> List[Dict[str, Any]]:
        """Get action history"""
        return self.authorizations["history"]
    
    def cleanup_expired(self) -> int:
        """Remove expired authorizations"""
        count = 0
        now = datetime.now()
        for auth in self.authorizations["targets"]:
            if auth["status"] == "active":
                try:
                    expires_at = datetime.fromisoformat(auth["expires_at"])
                    if now > expires_at:
                        auth["status"] = "expired"
                        count += 1
                except Exception:
                    continue
        if count > 0:
            self.save_authorizations()
        return count
