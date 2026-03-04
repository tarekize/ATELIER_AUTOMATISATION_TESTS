# 🚀 Guide de Déploiement - Tests API IPStack

## 📋 Prérequis

- Compte PythonAnywhere (gratuit ou payant)
- Clé API IPStack (gratuite sur https://ipstack.com)
- Repository GitHub

## 🔧 Configuration Locale

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration de la clé API

**Méthode 1 : Variable d'environnement (recommandée)**
```bash
# Windows (PowerShell)
$env:IPSTACK_API_KEY = "your_api_key_here"

# Linux/Mac
export IPSTACK_API_KEY="your_api_key_here"
```

**Méthode 2 : Fichier .env**
Créer un fichier `.env` :
```
IPSTACK_API_KEY=your_api_key_here
```

### 3. Test local
```bash
python flask_app.py
# Accéder à http://localhost:5000/dashboard
```

## 🌐 Déploiement sur PythonAnywhere

### Étape 1 : Configuration de base

1. **Accédez à PythonAnywhere** : https://www.pythonanywhere.com
2. **Web → Add a new web app**
3. Sélectionnez **Flask** et **Python 3.10** (ou autre)
4. Téléchargez le code de votre repository GitHub dans le répertoire source

### Étape 2 : Configurer les secrets GitHub

Dans votre repository GitHub, allez à **Settings → Secrets and variables → Actions** et créez 4 secrets :

| Secret | Exemple |
|--------|---------|
| **PA_USERNAME** | tarek |
| **PA_TOKEN** | Voir PythonAnywhere → Account → API Token |
| **PA_TARGET_DIR** | /home/tarek/myapp |
| **PA_WEBAPP_DOMAIN** | tarek.pythonanywhere.com |
| **IPSTACK_API_KEY** | votre_clé_api |

### Étape 3 : Configuration WSGI

Editez le fichier **WSGI** dans PythonAnywhere :

```python
import os
import sys

path = '/home/izerrouken/myapp'
if path not in sys.path:
    sys.path.append(path)

os.environ['IPSTACK_API_KEY'] = 'YOUR_API_KEY'  # Remplacer par votre clé

from flask_app import app as application
```

### Étape 4 : Installation des paquets

Via **Web Console** de PythonAnywhere :
```bash
cd /home/izerrouken/myapp
pip install -r requirements.txt
```

### Étape 5 : Planifier l'exécution des tests

Via **Scheduled tasks** dans PythonAnywhere, créer une tâche :

**Heure** : Chaque 5 minutes (ou moins fréquent)

**Commande** :
```bash
cd /home/izerrouken/myapp && /usr/bin/python3.10 -c "
from tester.runner import TestRunner
from storage import TestStorage
import os

api_key = os.getenv('IPSTACK_API_KEY')
runner = TestRunner()
report = runner.run(api_key)
storage = TestStorage()
storage.save_run(report)
"
```

**Alternative avec curl** (plus simple) :
```bash
curl -s https://izerrouken.pythonanywhere.com/run
```

## 📊 URLs disponibles

Après déploiement :

| URL | Description |
|-----|-------------|
| `https://izerrouken.pythonanywhere.com/` | Dashboard principal |
| `https://izerrouken.pythonanywhere.com/dashboard` | Résultats et historique |
| `https://izerrouken.pythonanywhere.com/run` | Déclencher tests manuellement |
| `https://izerrouken.pythonanywhere.com/health` | État de santé (JSON) |
| `https://izerrouken.pythonanywhere.com/api/runs` | Historique (JSON) |
| `https://izerrouken.pythonanywhere.com/api/statistics` | Statistiques (JSON) |

## 🔍 Troubleshooting

### Logs d'accès et d'erreur

```
Access log: https://izerrouken.pythonanywhere.com/access.log
Error log: https://izerrouken.pythonanywhere.com/error.log
Server log: https://izerrouken.pythonanywhere.com/server.log
```

### Problèmes courants

**❌ "ModuleNotFoundError: No module named 'tester'"**
- Vérifier que le dossier `tester/` contient `__init__.py`
- Vérifier le chemin dans sys.path du WSGI

**❌ "IPSTACK_API_KEY not found"**
- Ajouter la variable d'environnement dans le fichier WSGI
- Ou configurer via PythonAnywhere → Web → Environment variables

**❌ "Connection refused" ou "Timeout"**
- Vérifier la clé API IPStack
- Vérifier le rate limiting (limité à 10 req/min gratuit)
- Consulter les logs via URLs ci-dessus

**❌ "No module named 'requests'"**
```bash
pip install --user requests
```

## ✅ Checklist opérationnelle

- [ ] Repository GitHub forké
- [ ] Secrets configurés dans GitHub
- [ ] Code déployé sur PythonAnywhere
- [ ] Fichier WSGI configuré
- [ ] Clé API IPStack configurée
- [ ] Tâche planifiée active
- [ ] Dashboard accessible
- [ ] Tests s'exécutent automatiquement
- [ ] Logs consultables

## 📝 Notes importantes

1. **Rate limiting** : IPStack gratuit = 10 req/min. Ne pas exécuter plus souvent
2. **Base de données** : SQLite local, préserver le fichier `test_results.db`
3. **Sécurité** : Ne jamais committer votre clé API. Utiliser les Secrets GitHub
4. **Historique** : Les anciens runs (>30j) sont automatiquement supprimés

---
Besoin d'aide ? Consultez les logs : https://izerrouken.pythonanywhere.com/error.log
