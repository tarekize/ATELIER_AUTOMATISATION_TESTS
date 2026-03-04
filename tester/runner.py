"""
Exécuteur de tests et calcul des métriques QoS
Gère : exécution tests, calcul latence (avg/p95), taux erreur, horodatage
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
import statistics
import os
import json
from tester.client import APIClient
from tester.tests import IPStackTester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRunner:
    """Exécute les tests IPStack et calcule les métriques"""
    
    def __init__(self, base_url: str = "https://api.ipstack.com/api"):
        self.base_url = base_url
        self.client = APIClient(base_url, timeout=5, max_retries=1)
        self.tester = IPStackTester(self.client)
    
    def run(self, api_key: str) -> Dict[str, Any]:
        """
        Exécute la suite de tests complète
        Returns: dict avec résultats, métriques et timestamp
        """
        logger.info("=== Début exécution tests IPStack ===")
        
        # Exécuter les tests
        test_results = self.tester.run_all_tests(api_key)
        
        # Calculer les métriques
        metrics = self._calculate_metrics(test_results)
        
        # Créer le rapport
        run_report = {
            "api": "IPStack",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "passed": metrics["passed"],
                "failed": metrics["failed"],
                "total": metrics["total"],
                "pass_rate": metrics["pass_rate"],
                "error_rate": metrics["error_rate"],
                "latency_ms_avg": metrics["latency_avg"],
                "latency_ms_p95": metrics["latency_p95"]
            },
            "tests": test_results
        }
        
        logger.info(f"✅ Tests complétés: {metrics['passed']}/{metrics['total']} réussis")
        logger.info(f"📊 Latence moyenne: {metrics['latency_avg']:.2f}ms, P95: {metrics['latency_p95']:.2f}ms")
        
        return run_report
    
    def _calculate_metrics(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les métriques de QoS"""
        total = len(test_results)
        passed = sum(1 for t in test_results if t["status"] == "PASS")
        failed = total - passed
        
        # Latence - filtrer les latences invalides
        latencies = [t["latency_ms"] for t in test_results if isinstance(t["latency_ms"], (int, float)) and t["latency_ms"] > 0]
        
        if latencies:
            latency_avg = statistics.mean(latencies)
            latency_p95 = self._calculate_percentile(latencies, 95)
        else:
            latency_avg = 0
            latency_p95 = 0
        
        return {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0,
            "error_rate": failed / total if total > 0 else 0,
            "latency_avg": latency_avg,
            "latency_p95": latency_p95
        }
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calcule le percentile avec gestion des cas limites"""
        if not values or len(values) == 0:
            return 0
        
        sorted_values = sorted(values)
        
        # Si une seule valeur, la retourner
        if len(sorted_values) == 1:
            return sorted_values[0]
        
        # Calculer l'index
        index = (percentile / 100.0) * len(sorted_values)
        
        # Si index est exact et correspond a un element
        if index == int(index):
            idx = int(index) - 1
            if 0 <= idx < len(sorted_values):
                return sorted_values[idx]
            return sorted_values[-1]
        
        # Interpolation entre deux valeurs
        lower_idx = int(index)
        upper_idx = int(index) + 1
        
        # Assurer que les indices sont valides
        if lower_idx >= len(sorted_values):
            return sorted_values[-1]
        if upper_idx >= len(sorted_values):
            return sorted_values[-1]
        
        lower = sorted_values[lower_idx]
        upper = sorted_values[upper_idx]
        return lower + (upper - lower) * (index - int(index))
