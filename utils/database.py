"""
Database utility functions for ByteBreaker
"""
import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


class DatabaseManager:
    """Database manager for ByteBreaker"""
    
    def __init__(self, db_path: str = "data/bytebreaker.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self) -> None:
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Database connection failed: {e}")
    
    def _create_tables(self) -> None:
        """Create database tables"""
        if not self.conn:
            return
        
        try:
            # Scans table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    scan_type TEXT NOT NULL,
                    results TEXT,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # Vulnerabilities table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id INTEGER,
                    type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    target TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (scan_id) REFERENCES scans (id)
                )
            """)
            
            # Authorizations table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS authorizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    authorized_by TEXT NOT NULL,
                    authorized_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            
            # Reports table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            self.conn.commit()
        except Exception as e:
            print(f"Table creation failed: {e}")
    
    def save_scan(self, target: str, scan_type: str, results: Dict[str, Any]) -> int:
        """Save scan results to database"""
        if not self.conn:
            return -1
        
        try:
            self.cursor.execute("""
                INSERT INTO scans (target, scan_type, results, timestamp)
                VALUES (?, ?, ?, ?)
            """, (target, scan_type, json.dumps(results), datetime.now().isoformat()))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Failed to save scan: {e}")
            return -1
    
    def save_vulnerability(self, scan_id: int, vuln_type: str, severity: str,
                          title: str, description: str, target: str) -> int:
        """Save vulnerability to database"""
        if not self.conn:
            return -1
        
        try:
            self.cursor.execute("""
                INSERT INTO vulnerabilities 
                (scan_id, type, severity, title, description, target, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (scan_id, vuln_type, severity, title, description, 
                  target, datetime.now().isoformat()))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Failed to save vulnerability: {e}")
            return -1
    
    def get_scans(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scans from database"""
        if not self.conn:
            return []
        
        try:
            self.cursor.execute("""
                SELECT * FROM scans ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Failed to get scans: {e}")
            return []
    
    def get_vulnerabilities(self, scan_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get vulnerabilities from database"""
        if not self.conn:
            return []
        
        try:
            if scan_id:
                self.cursor.execute("""
                    SELECT * FROM vulnerabilities WHERE scan_id = ?
                """, (scan_id,))
            else:
                self.cursor.execute("SELECT * FROM vulnerabilities")
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Failed to get vulnerabilities: {e}")
            return []
    
    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
