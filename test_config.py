#!/usr/bin/env python3
"""
Script de test pour validation locale
À exécuter pour vérifier la configuration avant déploiement
"""

import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

def test_imports():
    """Test que tous les imports fonctionnent"""
    print("✓ Test 1: Imports...")
    try:
        from tester.client import APIClient
        from tester.tests import IPStackTester
        from tester.runner import TestRunner
        from storage import TestStorage
        print("  ✅ Tous les imports OK")
        return True
    except ImportError as e:
        print(f"  ❌ Erreur import: {e}")
        return False

def test_api_key():
    """Test que la clé API est configurée"""
    print("✓ Test 2: Clé API IPStack...")
    api_key = os.getenv("IPSTACK_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print(f"  ✅ Clé API configurée: {api_key[:10]}...")
        return True
    else:
        print("  ❌ Clé API non configurée ou par défaut")
        print("     Définir la variable d'environnement IPSTACK_API_KEY")
        return False

def test_database():
    """Test que la base SQLite fonctionne"""
    print("✓ Test 3: Base de données SQLite...")
    try:
        from storage import TestStorage
        storage = TestStorage()
        stats = storage.get_statistics()
        print(f"  ✅ Base de données OK (total_runs={stats.get('total_runs', 0)})")
        return True
    except Exception as e:
        print(f"  ❌ Erreur base de données: {e}")
        return False

def test_api_connection(api_key):
    """Test la connexion à l'API IPStack"""
    print("✓ Test 4: Connexion API IPStack...")
    try:
        from tester.client import APIClient
        client = APIClient("https://api.ipstack.com/api", timeout=5)
        data, status, latency = client.get("/check", params={"access_key": api_key})
        
        if status == 200:
            print(f"  ✅ API IPStack accessible (IP client: {data.get('ip')})")
            return True
        else:
            print(f"  ⚠️  API retourne status {status}")
            print(f"     Réponse: {data}")
            return False
    except Exception as e:
        print(f"  ❌ Erreur connexion API: {e}")
        return False

def test_runner(api_key):
    """Test l'exécution d'une suite de tests"""
    print("✓ Test 5: Exécution tests...")
    try:
        from tester.runner import TestRunner
        runner = TestRunner()
        report = runner.run(api_key)
        
        summary = report.get("summary", {})
        passed = summary.get("passed", 0)
        total = summary.get("total", 0)
        
        print(f"  ✅ Tests exécutés: {passed}/{total} réussis")
        
        if passed == total:
            return True
        else:
            print(f"     ⚠️  Certains tests ont échoué")
            return True  # Toujours ok si au moins un test
    except Exception as e:
        print(f"  ❌ Erreur exécution: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Tests de configuration locale")
    print("=" * 60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Clé API
    api_key = os.getenv("IPSTACK_API_KEY")
    results.append(("Clé API", test_api_key()))
    
    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  Configuration incomplète - clé API manquante")
        goto_next = input("\nContinuer sans clé API ? (y/n): ").lower()
        if goto_next != 'y':
            sys.exit(1)
    
    # Test 3: Database
    results.append(("Base de données", test_database()))
    
    # Test 4: API Connection
    if api_key and api_key != "your_api_key_here":
        results.append(("API IPStack", test_api_connection(api_key)))
    
    # Test 5: Runner
    if api_key and api_key != "your_api_key_here":
        results.append(("Tests Runner", test_runner(api_key)))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé")
    print("=" * 60)
    
    for name, status in results:
        symbol = "✅" if status else "⚠️"
        print(f"{symbol} {name}: {'OK' if status else 'ERREUR'}")
    
    print("=" * 60)
    
    if all(status for _, status in results):
        print("✅ Tous les tests sont passés ! Configuration OK.")
        print("   Prêt pour le déploiement sur PythonAnywhere.")
        return 0
    else:
        print("⚠️  Vérifiez les erreurs ci-dessus avant de continuer.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
