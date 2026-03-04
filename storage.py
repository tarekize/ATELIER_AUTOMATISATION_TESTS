"""
Gestion de la persistance avec SQLite
Sauvegarde et récupère les historiques de tests
"""

import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestStorage:
    """Gère la base SQLite pour les résultats de tests"""
    
    DB_PATH = "test_results.db"
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Crée les tables si elles n'existent pas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table principale pour les runs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    failed INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    pass_rate REAL NOT NULL,
                    error_rate REAL NOT NULL,
                    latency_avg REAL NOT NULL,
                    latency_p95 REAL NOT NULL,
                    full_report TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"Base de données initialisée: {self.db_path}")
        except Exception as e:
            logger.error(f"Erreur initialisation DB: {e}")
    
    def save_run(self, report: Dict[str, Any]) -> int:
        """
        Sauvegarde un rapport de test
        Returns: id du run inséré
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            summary = report.get("summary", {})
            
            cursor.execute("""
                INSERT INTO test_runs (
                    api_name, timestamp, passed, failed, total,
                    pass_rate, error_rate, latency_avg, latency_p95,
                    full_report
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                report.get("api", "Unknown"),
                report.get("timestamp", ""),
                summary.get("passed", 0),
                summary.get("failed", 0),
                summary.get("total", 0),
                summary.get("pass_rate", 0),
                summary.get("error_rate", 0),
                summary.get("latency_ms_avg", 0),
                summary.get("latency_ms_p95", 0),
                json.dumps(report)
            ))
            
            run_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Run sauvegardé avec id: {run_id}")
            return run_id
        
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return -1
    
    def get_latest_run(self) -> Optional[Dict[str, Any]]:
        """Récupère le dernier run"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT full_report FROM test_runs
                ORDER BY created_at DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Erreur lecture dernier run: {e}")
            return None
    
    def get_all_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupère les N derniers runs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT full_report FROM test_runs
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [json.loads(row[0]) for row in rows]
        except Exception as e:
            logger.error(f"Erreur lecture runs: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère statistiques générales (derniers 10 runs)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_runs,
                    AVG(pass_rate) as avg_pass_rate,
                    AVG(error_rate) as avg_error_rate,
                    AVG(latency_avg) as avg_latency,
                    MIN(latency_avg) as min_latency,
                    MAX(latency_avg) as max_latency
                FROM test_runs
                WHERE created_at >= datetime('now', '-7 days')
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "total_runs": row[0] or 0,
                    "avg_pass_rate": row[1] or 0,
                    "avg_error_rate": row[2] or 0,
                    "avg_latency_ms": row[3] or 0,
                    "min_latency_ms": row[4] or 0,
                    "max_latency_ms": row[5] or 0
                }
            return {}
        except Exception as e:
            logger.error(f"Erreur calcul stats: {e}")
            return {}
    
    def delete_old_runs(self, days: int = 30) -> None:
        """Nettoie les runs > N jours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM test_runs
                WHERE created_at < datetime('now', '-' || ? || ' days')
            """, (days,))
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            logger.info(f"Supprimé {deleted} anciens runs")
        except Exception as e:
            logger.error(f"Erreur suppression: {e}")
