# 🚀 Quickstart Guide - Atelier Tests Automatisés

## ⚡ En 5 minutes

### 1. Configuration locale
```bash
# Créer .env depuis exemple
cp .env.example .env

# Ajouter votre clé API IPStack
# Éditer .env et ajouter : IPSTACK_API_KEY=votre_clé
```

### 2. Installer dépendances
```bash
pip install -r requirements.txt
```

### 3. Tester localement
```bash
# Validation config
python test_config.py

# Ou test manuel
python manual_test.py

# Lancer l'app Flask
python flask_app.py
# → http://localhost:5000
```

---

## 📋 Fichiers Clés Expliqués

| Fichier | Rôle | Importance |
|---------|------|-----------|
| `flask_app.py` | Application principale | 🔴 CRITIQUE |
| `tester/client.py` | HTTP wrapper (timeout, retry) | 🔴 CRITIQUE |
| `tester/tests.py` | Suite des 6 tests | 🟠 IMPORTANTE |
| `tester/runner.py` | Orchestration + métriques | 🟠 IMPORTANTE |
| `storage.py` | SQLite persistance | 🟠 IMPORTANTE |
| `templates/dashboard.html` | UI résultats | 🟠 IMPORTANTE |
| `requirements.txt` | Dépendances | 🔴 CRITIQUE |
| `.env` | Variables d'environnement | 🔴 CRITIQUE |

---

## 🔑 Obtenir une Clé API IPStack

1. Aller sur https://ipstack.com
2. S'inscrire (gratuit)
3. Copier la clé de la page de Dashboard
4. Ajouter dans `.env` : `IPSTACK_API_KEY=votre_clé`

---

## 🌐 Déployer sur PythonAnywhere

### Étape 1: Créer compte & secrets GitHub
1. Compte PythonAnywhere : https://www.pythonanywhere.com
2. Dans GitHub repo → Settings → Secrets → Ajouter 5 secrets :
   - `PA_USERNAME` : votre username PythonAnywhere
   - `PA_TOKEN` : voir PythonAnywhere → Account → API token
   - `PA_TARGET_DIR` : `/home/USERNAME/myapp`
   - `PA_WEBAPP_DOMAIN` : `username.pythonanywhere.com`
   - `IPSTACK_API_KEY` : votre clé IPStack

### Étape 2: Configurer WSGI
Dans PythonAnywhere → Web → WSGI configuration file :
```python
import os, sys
os.environ['IPSTACK_API_KEY'] = 'YOUR_KEY'
path = '/home/username/myapp'
sys.path.insert(0, path)
from flask_app import app as application
```

### Étape 3: Push et déploiement auto
```bash
git add .
git commit -m "Initial tests automation"
git push origin main
# → GitHub Actions déclenche le déploiement automatiquement
```

### Étape 4: Planifier l'exécution
Dans PythonAnywhere → Scheduled tasks → Create new task
- **Heure** : Toutes les 5 minutes
- **Commande** :
```bash
curl -s https://username.pythonanywhere.com/run
```

---

## ✅ URLs Une Fois Déployées

```
Dashboard       → https://username.pythonanywhere.com/
Exécution       → https://username.pythonanywhere.com/run
Santé (Health)  → https://username.pythonanywhere.com/health
Historique API  → https://username.pythonanywhere.com/api/runs
Stats API       → https://username.pythonanywhere.com/api/statistics
```

---

## 🔍 Débogag Rapide

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: tester` | Vérifier `tester/__init__.py` existe |
| `API Key not found` | Configurer `.env` ou variable d'envmt |
| `429 Rate Limit` | IPStack gratuit = 10 req/min, augmenter délai |
| `Connection refused` | Vérifier clé API ou internet |

Consulter logs : https://username.pythonanywhere.com/error.log

---

## 📊 Structure des Résultats

Chaque run produit un rapport JSON :
```json
{
  "api": "IPStack",
  "timestamp": "2026-03-04T10:30:00",
  "summary": {
    "passed": 6,
    "failed": 0,
    "pass_rate": 1.0,
    "error_rate": 0.0,
    "latency_ms_avg": 245.3,
    "latency_ms_p95": 520.1
  },
  "tests": [
    {"name": "API Reachable", "status": "PASS", "latency_ms": 245}
    // ...
  ]
}
```

Sauvegardé en SQLite → Historique affiché en dashboard

---

## 📞 Support

- **Logs** : PythonAnywhere → Web → Error log
- **Docs API** : https://ipstack.com/documentation
- **GitHub Issues** : Créer un issue dans votre repo

---

**Bonne chance ! 🎓**
