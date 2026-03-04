#!/usr/bin/env python3
"""
Script rapide pour tester manuellement l'API IPStack
Complément au test_config.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 60)
    print("🧪 Test Manuel API IPStack")
    print("=" * 60)
    
    api_key = os.getenv("IPSTACK_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        print("❌ Clé API non configurée")
        print("\nConfigurer ainsi :")
        print("  export IPSTACK_API_KEY='votre_clé'")
        return 1
    
    # Test 1: Test HTTP simple
    print("\n1️⃣  Test HTTP Simple...")
    try:
        import requests
        response = requests.get(
            "https://api.ipstack.com/api/check",
            params={"access_key": api_key},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   IP détectée: {data.get('ip')}")
        print(f"   Pays: {data.get('country_code')} ({data.get('country_name')})")
        print(f"   Ville: {data.get('city')}")
        print("   ✅ HTTP OK")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 1
    
    # Test 2: Test Client Wrapper
    print("\n2️⃣  Test Client Wrapper...")
    try:
        from tester.client import APIClient
        client = APIClient("https://api.ipstack.com/api")
        data, status, latency = client.get("/check", params={"access_key": api_key})
        print(f"   Status: {status}")
        print(f"   Latence: {latency:.2f}ms")
        print(f"   IP: {data.get('ip')}")
        print("   ✅ Client OK")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 1
    
    # Test 3: Suite complète
    print("\n3️⃣  Test Suite Complète...")
    try:
        from tester.runner import TestRunner
        runner = TestRunner()
        report = runner.run(api_key)
        
        summary = report.get("summary", {})
        print(f"   Tests passés: {summary.get('passed')}/{summary.get('total')}")
        print(f"   Taux réussite: {summary.get('pass_rate')*100:.1f}%")
        print(f"   Latence avg: {summary.get('latency_ms_avg'):.2f}ms")
        print(f"   Latence p95: {summary.get('latency_ms_p95'):.2f}ms")
        print("   ✅ Suite OK")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 1
    
    # Test 4: Sauvegarde BDD
    print("\n4️⃣  Test Sauvegarde BDD...")
    try:
        from storage import TestStorage
        storage = TestStorage()
        run_id = storage.save_run(report)
        print(f"   Run ID: {run_id}")
        
        latest = storage.get_latest_run()
        print(f"   Dernière exécution: {latest.get('timestamp')}")
        print("   ✅ BDD OK")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests sont passés!")
    print("=" * 60)
    
    print("\n📊 Prochaines étapes:")
    print("  1. Accéder au dashboard: http://localhost:5000/dashboard")
    print("  2. Lancer l'app Flask: python flask_app.py")
    print("  3. Déployer sur PythonAnywhere via GitHub")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
