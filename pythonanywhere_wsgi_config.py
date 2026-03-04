"""
WSGI Configuration pour PythonAnywhere
À adapter au chemin réel de votre installation

INSTRUCTIONS:
1. Accéder à PythonAnywhere -> Web -> WSGI configuration file
2. Remplacer le contenu par ce fichier
3. Adapter le chemin /home/izerrouken/myapp à votre path réel
4. Configurer la clé API IPStack
5. Relancer votre application web
"""

import os
import sys
import logging

# ================== CONFIGURATION ==================

# Remplacer par le chemin réel de votre application
PROJECT_PATH = '/home/izerrouken/myapp'

# Configuration variable d'environnement
os.environ['IPSTACK_API_KEY'] = 'YOUR_API_KEY_HERE'

# =====================================================

# Ajouter le chemin du projet au sys.path
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"Chargement Flask app depuis {PROJECT_PATH}")

# Importer l'application Flask
try:
    from flask_app import app as application
    logger.info("✅ Application Flask chargée avec succès")
except Exception as e:
    logger.error(f"❌ Erreur chargement Flask: {e}")
    raise

# Les variables nommées 'application' et 'from_wsgi' sont requises par PythonAnywhere
application.wsgi_app = application.wsgi_app
