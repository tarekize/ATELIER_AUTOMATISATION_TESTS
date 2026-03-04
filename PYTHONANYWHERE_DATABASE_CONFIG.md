# 🌐 Configuration PythonAnywhere - Guide Complet

## 📋 Configuration de la Base de Données (DATABASE_PATH)

Vous vous demandez comment configurer `DATABASE_PATH=/home/izerrouken/myapp/test_results.db` sur PythonAnywhere ?

Voici comment faire :

---

## 1️⃣ ACTUELLEMENT (Configuration locale)

**Votre .env contient :**
```dotenv
# Clé API
IPSTACK_API_KEY=fe6c3714873e3d1724bdfcba337a0382

# Configuration Flask
FLASK_DEBUG=True
FLASK_ENV=development

# Configuration PythonAnywhere (COMMENTÉE pour l'instant)
# DATABASE_PATH=/home/izerrouken/myapp/test_results.db
```

**Comportement local :**
- La base de données est créée automatiquement en `test_results.db` dans le dossier courant ✅
- Vous n'avez RIEN à faire pour le moment
- Laissez `DATABASE_PATH` en commentaire (comme c'est actuellement)

---

## 2️⃣ DÉPLOIEMENT SUR PYTHONANYWHERE

Quand vous déployez sur PythonAnywhere, il y a **3 configurations possibles** :

### Option A : Configuration Automatique (RECOMMANDÉE) ⭐

**Aucune action requise !**

Le code fait ceci automatiquement :
```python
# Dans storage.py
DB_PATH = "test_results.db"  # Chemin local

# Lors du déploiement sur PythonAnywhere
# → La base est créée en /home/izerrouken/myapp/test_results.db
# → C'est automatique grâce au répertoire source
```

✅ **Avantage** : Zéro configuration, ça marche tout seul  
✅ **Inconvénient** : Aucun

---

### Option B : Configuration Explicite (Si vous voulez personnaliser)

Si vous voulez absolument spécifier le chemin :

#### Étape 1 : Éditer .env
```dotenv
# En DEV (local)
DATABASE_PATH=test_results.db

# En PRODUCTION (PythonAnywhere) - Laisser en commentaire, voir Étape 2
# DATABASE_PATH=/home/izerrouken/myapp/test_results.db
```

#### Étape 2 : Modifier storage.py
```python
# storage.py - Ligne ~14

import os

DB_PATH = os.getenv("DATABASE_PATH", "test_results.db")

class TestStorage:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        # ...
```

#### Étape 3 : Sur PythonAnywhere - Fichier WSGI
```python
# Dans le fichier WSGI (PythonAnywhere → Web → WSGI configuration)

import os
import sys

# Configuration
os.environ['IPSTACK_API_KEY'] = 'YOUR_KEY'
os.environ['DATABASE_PATH'] = '/home/izerrouken/myapp/test_results.db'  # ← AJOUTER

path = '/home/izerrouken/myapp'
sys.path.insert(0, path)

from flask_app import app as application
```

✅ **Avantage** : Contrôle total du chemin  
⚠️ **Inconvénient** : Configuration supplémentaire

---

### Option C : Configuration via Variable d'Environnement GitHub

Pour une approche DevOps complète :

#### Dans GitHub Secrets
```
DATABASE_PATH = /home/izerrouken/myapp/test_results.db
```

#### Dans le WSGI
```python
import os

db_path = os.getenv('DATABASE_PATH', 'test_results.db')
os.environ['DATABASE_PATH'] = db_path
```

✅ **Avantage** : Configuration centralisée  
⚠️ **Inconvénient** : Plus complexe

---

## 3️⃣ STRUCTURE DES RÉPERTOIRES PYTHONANYWHERE

**Votre structure sur PythonAnywhere sera :**

```
/home/izerrouken/
├── myapp/                           ← PA_TARGET_DIR
│   ├── flask_app.py
│   ├── storage.py
│   ├── requirements.txt
│   ├── test_results.db              ← Base de données SQLite 📊
│   ├── tester/
│   ├── templates/
│   └── .env
├── .pythonanywhere.com_wsgi.py      ← Fichier WSGI
└── test_results.db                  ← Copie si DATABASE_PATH simple chemin
```

**Votre clé donne :**
- `PA_USERNAME` = izerrouken
- `PA_TARGET_DIR` = /home/izerrouken/myapp
- `PA_WEBAPP_DOMAIN` = izerrouken.pythonanywhere.com

---

## 4️⃣ VÉRIFIER QUE ÇA MARCHE

### Local (Avant déploiement)
```bash
python test_config.py
# → Doit afficher ✅ Base de données OK
# → Crée test_results.db localement
```

### Sur PythonAnywhere (Après déploiement)

**1. Vérifier le fichier existe**
```bash
# Via Web Console PythonAnywhere
cd /home/izerrouken/myapp
ls -la test_results.db
# → Doit afficher le fichier
```

**2. Tester la base de données**
```bash
# Via Web Console PythonAnywhere
cd /home/izerrouken/myapp
python3 -c "
from storage import TestStorage
s = TestStorage()
print('✅ Base OK')
stats = s.get_statistics()
print(f'Runs: {stats}')
"
```

**3. Vérifier via Dashboard**
```
https://izerrouken.pythonanywhere.com/dashboard
→ Doit afficher les résultats de tests
```

**4. Vérifier via API**
```bash
curl https://izerrouken.pythonanywhere.com/api/statistics
# → Doit retourner un JSON avec les stats
```

---

## 5️⃣ PERMISSION FICHIERS (Si erreur)

Si vous recevez `permission denied` :

**Via Web Console PythonAnywhere**
```bash
cd /home/izerrouken/myapp
chmod 644 test_results.db          # Lecture/écriture propietaire
chmod 755 .                         # Dossier exécutable
```

---

## 6️⃣ NETTOYAGE AUTOMATIQUE

**Le code nettoie automatiquement les anciens runs (>30 jours)** :

```python
# Dans storage.py
storage.delete_old_runs(days=30)
```

**Pour ajuster :**
```python
# Flask app.py - Lors de chaque run
storage.delete_old_runs(days=7)  # Garder seulement 7 jours
```

---

## 7️⃣ BACKUP DE LA BASE DE DONNÉES

**Recommandé :** Sauvegarder régulièrement votre base

**Via Web Console PythonAnywhere**
```bash
# Sauvegarde
cp /home/izerrouken/myapp/test_results.db /home/izerrouken/test_results.db.backup

# Télécharger ensuite via Files → Download
```

---

## ⚡ RÉSUMÉ RAPIDE

| Scenario | Action | DATABASE_PATH |
|----------|--------|---------------|
| **Développement local** | Aucune | `test_results.db` |
| **Déploiement PythonAnywhere** | Automatique | Auto dans `/home/izerrouken/myapp/` |
| **Personnalisation** | Éditer WSGI | `/home/izerrouken/myapp/test_results.db` |

**Pour 99% des cas : Laissez tel quel, c'est automatique ! ✅**

---

## 🔍 DÉPANNAGE

| Problème | Solution |
|----------|----------|
| "No such file or database" | Base pas créée → lancer `/run` endpoint |
| "Permission denied" | `chmod 644 test_results.db` |
| "Disk quota exceeded" | Supprimer anciens runs ou augmenter quota |
| Dashboard vide | Base vide → cliquer "Exécuter tests" d'abord |
| Stats ne s'actualisent pas | Clear browser cache + refresh |

---

## 📝 CHECKLIST CONFIGURATION BASE DE DONNEES

- [ ] `.env` correct localement (ou non configuré si auto)
- [ ] `test_results.db` créé après `python flask_app.py`
- [ ] `test_config.py` passe sans erreur
- [ ] Code déployé sur PythonAnywhere
- [ ] WSGI configuré
- [ ] Premier run de tests déclenché
- [ ] Dashboard affiche les résultats
- [ ] Fichier `test_results.db` visible dans `/home/izerrouken/myapp/`

---

**Besoin d'aide ?** Consultez DEPLOYMENT.md ou vérifiez les logs : `/error.log`
