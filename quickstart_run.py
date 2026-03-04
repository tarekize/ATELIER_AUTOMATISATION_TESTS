#!/usr/bin/env python3
"""
🚀 TEST ULTRA-RAPIDE EN LIGNE
Lance en une commande la validation complète + l'app
"""

if __name__ == "__main__":
    import os
    import sys
    import subprocess
    from pathlib import Path
    
    print("=" * 70)
    print("🚀 DÉMARRAGE RAPIDE - Test Complet")
    print("=" * 70)
    
    # Vérifier .env existe
    if not Path(".env").exists():
        print("\n⚠️  .env non trouvé. Création depuis .env.example...")
        if Path(".env.example").exists():
            with open(".env.example") as f:
                example = f.read()
            with open(".env", "w") as f:
                f.write(example)
            print("✅ .env créé. À ÉDITER pour ajouter IPSTACK_API_KEY!")
        else:
            print("❌ .env.example non trouvé")
            sys.exit(1)
    
    # Vérifier requirements
    print("\n📦 Vérification dépendances...")
    try:
        import flask
        import requests
        print("✅ Dépendances OK (Flask, requests)")
    except ImportError:
        print("⚠️  Installation dépendances...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dépendances installées")
    
    # Vérifier structure
    print("\n📁 Vérification structure...")
    required = [
        "flask_app.py", 
        "storage.py", 
        "tester/client.py",
        "tester/tests.py",
        "tester/runner.py",
        "templates/dashboard.html",
        ".env"
    ]
    
    for f in required:
        if Path(f).exists():
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} MANQUANT")
    
    # Test config
    print("\n🔍 Test configuration...")
    try:
        api_key = os.getenv("IPSTACK_API_KEY") or ""
        if api_key and api_key != "your_api_key_here":
            print(f"  ✅ IPSTACK_API_KEY configurée ({'*' * 8}...)")
        else:
            print("  ⚠️  IPSTACK_API_KEY non configurée ou par défaut")
            print("     → Éditer .env et ajouter : IPSTACK_API_KEY=votre_clé")
    except Exception as e:
        print(f"  ❌ Erreur config: {e}")
    
    # Imports test
    print("\n🐍 Test imports...")
    try:
        from tester.client import APIClient
        from tester.tests import IPStackTester
        from tester.runner import TestRunner
        from storage import TestStorage
        print("  ✅ Tous les imports OK")
    except ImportError as e:
        print(f"  ❌ Erreur import: {e}")
        sys.exit(1)
    
    # Prompt lancement
    print("\n" + "=" * 70)
    print("✅ VALIDATION TERMINÉE - Prêt à démarrer !")
    print("=" * 70)
    
    print("\nCommande démarrage :")
    print("  python flask_app.py")
    print("\nPuis accéder à :")
    print("  http://localhost:5000/dashboard")
    
    # Optionnel : lancer directement
    response = input("\nLancer Flask maintenant ? (y/n): ").lower().strip()
    if response == 'y':
        print("\n🚀 Lancement Flask...")
        print("   (Ctrl+C pour arrêter)")
        try:
            subprocess.run([sys.executable, "flask_app.py"])
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt.")
    else:
        print("\nManuel :")
        print("  python flask_app.py")
