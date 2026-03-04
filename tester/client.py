"""
HTTP Client wrapper pour tester l'API IPStack
Gère : timeout, retries, mesure de latence, gestion erreurs 429/5xx
"""

import requests
import time
import logging
from typing import Dict, Tuple, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """Wrapper HTTP avec timeout, retry et mesure de latence"""
    
    def __init__(self, base_url: str, timeout: int = 5, max_retries: int = 1):
        """
        Args:
            base_url: URL de base de l'API
            timeout: Timeout en secondes (défaut 5s)
            max_retries: Nombre max de retries (défaut 1)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Crée une session avec retry strategy"""
        session = requests.Session()
        
        # Définir retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        return session
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Tuple[Dict, int, float]:
        """
        Effectue une requête GET
        Returns: (response_data, status_code, latency_ms)
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = time.time()
            response = self.session.get(url, params=params, timeout=self.timeout)
            latency_ms = (time.time() - start_time) * 1000
            
            logger.info(f"GET {url} -> {response.status_code} ({latency_ms:.2f}ms)")
            
            try:
                data = response.json()
            except:
                data = {"error": "Invalid JSON response"}
            
            return data, response.status_code, latency_ms
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout après {self.timeout}s pour {url}")
            return {"error": f"Timeout après {self.timeout}s"}, 0, self.timeout * 1000
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erreur connexion : {e}")
            return {"error": f"Connection error: {str(e)}"}, 0, 0
        
        except Exception as e:
            logger.error(f"Erreur inattendue : {e}")
            return {"error": str(e)}, 0, 0
