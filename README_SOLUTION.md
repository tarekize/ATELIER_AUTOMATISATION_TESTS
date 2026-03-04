------------------------------------------------------------------------------------------------------
🎯 Atelier "Testing as Code & API Monitoring" - Solution Complète
------------------------------------------------------------------------------------------------------

## 📋 Description du Projet

Automatisation complète de tests d'API publique (IPStack) avec :
- ✅ **6+ tests** validant contrat, robustesse et QoS
- ✅ **Gestion erreurs** : timeout, retry, code 429/5xx
- ✅ **Métriques QoS** : latence avg/p95, taux erreur, disponibilité
- ✅ **Dashboard** affichant résultats et historique
- ✅ **SQLite** persistant les runs et statistiques
- ✅ **Déploiement PythonAnywhere** avec exécution planifiée

---

## 📁 Structure du Projet

```
.
├── flask_app.py                 # Application Flask principale
├── storage.py                   # Gestion SQLite et persistance
├── requirements.txt             # Dépendances Python
├── API_CHOICE.md               # Documentation API choisie (IPStack)
├── DEPLOYMENT.md               # Guide complet de déploiement
├── test_config.py              # Script validation locale
├── pythonanywhere_wsgi_config.py # Template WSGI PythonAnywhere
├── .env.example                # Template variables d'environnement
├── .gitignore                  # Fichiers à ignorer
├── tester/
│   ├── __init__.py
│   ├── client.py               # Wrapper HTTP (timeout, retry, latence)
│   ├── tests.py                # Suite de 6 tests IPStack
│   └── runner.py               # Orchestration tests + calcul métriques
└── templates/
    └── dashboard.html          # Dashboard résultats en temps réel
```

---

## 🚀 Démarrage Rapide (Local)

### 1️⃣ Installation
```bash
# Cloner votre fork du repository
git clone https://github.com/YOUR_USERNAME/automation-tests.git
cd automation-tests

# Créer environnement virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer dépendances
pip install -r requirements.txt
```

### 2️⃣ Configuration Clé API
```bash
# Créer fichier .env depuis .env.example
cp .env.example .env

# Ajouter votre clé API IPStack
# IPSTACK_API_KEY=your_key_here
```

Obtenir la clé : https://ipstack.com (gratuit : 100 appels/mois)

### 3️⃣ Validation Locale
```bash
python test_config.py
```

### 4️⃣ Lancer l'application
```bash
python flask_app.py
# Accéder à http://localhost:5000/dashboard
```

---

## 📊 Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Redirige vers le dashboard |
| `/dashboard` | GET | 📊 Dashboard avec résultats et historique |
| `/run` | GET | ▶️ Déclenche les tests manuellement |
| `/health` | GET | 🏥 État de santé (JSON) |
| `/api/runs` | GET | 📜 Historique JSON |
| `/api/statistics` | GET | 📈 Statistiques JSON |

---

## 🧪 Suite de Tests (6+ tests)

### Tests Contrat
1. **API Reachable** - Vérifier HTTP 200 et réponse valide
2. **Required Fields** - Tous les champs obligatoires présents
3. **Field Types** - Types de données corrects
4. **JSON Content Type** - Réponse JSON valide

### Tests Robustesse
5. **Custom IP Test** - Lookup avec IP spécifique (8.8.8.8)
6. **Invalid API Key** - Gestion erreur clé invalide

### Métriques QoS
- Latence moyenne (ms)
- Latence P95 (percentile 95)
- Taux de réussite
- Taux d'erreur

---

## 🌐 Déploiement sur PythonAnywhere

**Consulter [DEPLOYMENT.md](DEPLOYMENT.md) pour instructions complètes**

Résumé rapide :
1. Créer compte PythonAnywhere
2. Configurer secrets GitHub (4 secrets : USERNAME, TOKEN, TARGET_DIR, DOMAIN)
3. Déployer code via Actions GitHub
4. Configurer fichier WSGI
5. Créer tâche planifiée pour exécution automatique

---

## ⚙️ Tâche Planifiée

Pour exécution automatique toutes les 5 minutes via PythonAnywhere Scheduled Tasks :

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

Ou simplement :
```bash
curl https://izerrouken.pythonanywhere.com/run
```

---

## 🔍 Troubleshooting

Les logs sont accessibles via :
- **Access log** : https://izerrouken.pythonanywhere.com/access.log
- **Error log** : https://izerrouken.pythonanywhere.com/error.log

### Problèmes courants

**ModuleNotFoundError: tester**
→ Vérifier `tester/__init__.py` existe
→ Vérifier sys.path dans fichier WSGI

**API Key not found**
→ Configurer variable d'environnement IPSTACK_API_KEY

**Rate Limit (429)**
→ IPStack gratuit : max 10 req/min
→ Espacer exécution tests (min 5-10 min)

---

## 📊 Barème / Évaluation (/20 points)

| Critère | Points | ✅ Status |
|---------|--------|----------|
| Choix API + contrat | 2 | ✅ IPStack documentée |
| Qualité tests | 6 | ✅ 6 tests implémentés |
| Robustesse | 4 | ✅ Timeout + retry + gestion erreurs |
| QoS Metrics | 4 | ✅ Latence + taux erreur + dispo |
| Restitution | 4 | ✅ Dashboard + historique + health |
| **BONUS** | +2 | ✅ Tâche planifiée + health endpoint |

---

## 📚 Ressources

- [IPStack Documentation](https://ipstack.com/documentation)
- [Public APIs List](https://github.com/public-apis/public-apis)
- [PythonAnywhere Hosting](https://www.pythonanywhere.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## ✅ Checklist Opérationnelle

- [ ] API_CHOICE.md complété
- [ ] Tests locaux passent (`python test_config.py`)
- [ ] Code committé sur GitHub
- [ ] Secrets configurés dans GitHub
- [ ] Application déployée sur PythonAnywhere
- [ ] WSGI configuré correctement
- [ ] Tâche planifiée créée
- [ ] Dashboard accessible en ligne
- [ ] Tests s'exécutent automatiquement
- [ ] Métriques affichées correctement

---

## 🎓 Auteur

**Étudiant** : Tarek Zerrouken  
**Atelier** : Automatisation Tests d'API  
**Niveau** : Bac+2 / Ingénieur  
**Durée** : ~120 minutes  
**Difficulté** : Moyenne
