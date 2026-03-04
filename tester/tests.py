"""
Tests pour l'API IPStack
Valide : contrat (champs, types), codes HTTP, robustesse, formats attendus

URL de l'API IPStack (plan gratuit) :
  - http://api.ipstack.com/check?access_key=CLE         → IP du client
  - http://api.ipstack.com/8.8.8.8?access_key=CLE       → IP spécifique
  
ATTENTION : plan gratuit = HTTP uniquement (pas HTTPS), pas de /api dans l'URL
"""

import logging
import time
from typing import Dict, Any, List, Tuple
from tester.client import APIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _is_ipstack_error(data: dict) -> bool:
    """Vérifie si la réponse IPStack est une erreur (success=false)"""
    return data.get("success") is False or "error" in data


def _get_ipstack_error_info(data: dict) -> str:
    """Extrait le message d'erreur IPStack"""
    if "error" in data:
        err = data["error"]
        return f"IPStack erreur {err.get('code', '?')}: {err.get('type', '?')} - {err.get('info', '')}"
    return "Réponse IPStack invalide"


class IPStackTester:
    """Suite de tests pour API IPStack"""
    
    REQUIRED_FIELDS = ["ip", "country_code", "city", "latitude", "longitude"]
    FIELD_TYPES = {
        "ip": str,
        "country_code": str,
        "city": str,
        "latitude": (int, float),
        "longitude": (int, float),
        "type": str,
    }
    TEST_DELAY = 1  # Delai entre les tests en secondes (pour eviter rate limit)
    
    def __init__(self, client: APIClient):
        self.client = client
        self.test_results: List[Dict[str, Any]] = []
    
    def run_all_tests(self, api_key: str) -> List[Dict[str, Any]]:
        """Exécute tous les tests et retourne les résultats"""
        self.test_results = []
        
        logger.info(f"Base URL utilisée: {self.client.base_url}")
        
        # Test 1: Vérifier status 200 et réponse valide
        self._test_api_reachable(api_key)
        time.sleep(self.TEST_DELAY)
        
        # Test 2: Vérifier champs obligatoires présents
        self._test_required_fields(api_key)
        time.sleep(self.TEST_DELAY)
        
        # Test 3: Vérifier types de données
        self._test_field_types(api_key)
        time.sleep(self.TEST_DELAY)
        
        # Test 4: Vérifier Content-Type est JSON
        self._test_json_content_type(api_key)
        time.sleep(self.TEST_DELAY)
        
        # Test 5: Tester avec IP personnalisée
        self._test_custom_ip(api_key, "8.8.8.8")
        time.sleep(self.TEST_DELAY)
        
        # Test 6: Tester cas d'erreur : clé API invalide
        self._test_invalid_api_key()
        
        return self.test_results
    
    def _test_api_reachable(self, api_key: str) -> None:
        """Test 1: API accessible et retourne 200 avec données IP"""
        name = "GET /check - API Reachable"
        try:
            data, status, latency = self.client.get("/check", params={"access_key": api_key})
            
            # Détecter erreur IPStack (ex: HTTPS sur plan gratuit)
            if _is_ipstack_error(data):
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": _get_ipstack_error_info(data)
                })
                return
            
            if status == 200 and "ip" in data:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": f"Status 200, IP client: {data.get('ip')}"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": f"Status {status}, réponse: {str(data)[:200]}"
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    
    def _test_required_fields(self, api_key: str) -> None:
        """Test 2: Tous les champs obligatoires sont présents"""
        name = "Required Fields Check"
        try:
            data, status, latency = self.client.get("/check", params={"access_key": api_key})
            
            # Détecter erreur IPStack
            if _is_ipstack_error(data):
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": _get_ipstack_error_info(data)
                })
                return
            
            missing_fields = [f for f in self.REQUIRED_FIELDS if f not in data]
            
            if not missing_fields:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": "Tous les champs obligatoires présents"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": f"Champs manquants: {', '.join(missing_fields)}"
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    
    def _test_field_types(self, api_key: str) -> None:
        """Test 3: Types de données correctes"""
        name = "Field Types Validation"
        try:
            data, status, latency = self.client.get("/check", params={"access_key": api_key})
            
            # Détecter erreur IPStack
            if _is_ipstack_error(data):
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": _get_ipstack_error_info(data)
                })
                return
            
            type_errors = []
            for field, expected_type in self.FIELD_TYPES.items():
                if field in data:
                    value = data[field]
                    # Accepter None pour certains champs optionnels
                    if value is not None and not isinstance(value, expected_type):
                        type_errors.append(f"{field}: attendu {expected_type.__name__ if hasattr(expected_type, '__name__') else expected_type}, reçu {type(value).__name__}")
            
            if not type_errors:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": "Tous les types sont corrects"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": "; ".join(type_errors)
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    
    def _test_json_content_type(self, api_key: str) -> None:
        """Test 4: Réponse est du JSON valide"""
        name = "JSON Content Type"
        try:
            data, status, latency = self.client.get("/check", params={"access_key": api_key})
            
            if isinstance(data, dict) and status == 200:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": "Réponse valide JSON"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": f"Réponse non-JSON ou status {status}"
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    
    def _test_custom_ip(self, api_key: str, ip_address: str) -> None:
        """Test 5: Tester avec IP spécifique (Google DNS 8.8.8.8)
        
        IPStack attend l'IP dans le chemin URL :
          http://api.ipstack.com/8.8.8.8?access_key=CLE
        """
        name = f"Custom IP Test ({ip_address})"
        try:
            # IPStack : l'IP va dans le path, PAS en query param
            data, status, latency = self.client.get(f"/{ip_address}", params={
                "access_key": api_key
            })
            
            # Détecter erreur IPStack
            if _is_ipstack_error(data):
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": _get_ipstack_error_info(data)
                })
                return
            
            if status == 200 and data.get("ip") == ip_address:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": f"IP {ip_address} trouvée, pays: {data.get('country_code')}"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": f"Status {status}, IP reçue: {data.get('ip', 'aucune')}"
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
    
    def _test_invalid_api_key(self) -> None:
        """Test 6: Erreur attendue avec clé API invalide"""
        name = "Invalid API Key Error Handling"
        try:
            data, status, latency = self.client.get("/check", params={"access_key": "invalid_key_12345"})
            
            # IPStack retourne {"success": false, "error": {...}} avec clé invalide
            if _is_ipstack_error(data) or status in [401, 403, 404]:
                self.test_results.append({
                    "name": name,
                    "status": "PASS",
                    "latency_ms": latency,
                    "details": f"Erreur correctement détectée (status {status})"
                })
            else:
                self.test_results.append({
                    "name": name,
                    "status": "FAIL",
                    "latency_ms": latency,
                    "details": f"Devrait retourner erreur, reçu status {status}"
                })
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": str(e)
            })
