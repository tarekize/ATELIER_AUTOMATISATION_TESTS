#!/usr/bin/env python3
"""
Vérification rapide : TOUT est en place ?
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Vérifie qu'un fichier existe"""
    if Path(path).exists():
        size = Path(path).stat().st_size
        print(f"  ✅ {description:50} ({size:,} bytes)")
        return True
    else:
        print(f"  ❌ {description:50} MANQUANT")
        return False

def check_directory(path, description):
    """Vérifie qu'un dossier existe"""
    if Path(path).is_dir():
        files = len(list(Path(path).glob("*")))
        print(f"  ✅ {description:50} ({files} files)")
        return True
    else:
        print(f"  ❌ {description:50} MANQUANT")
        return False

def main():
    print("=" * 80)
    print("🔍 VÉRIFICATION SOLUTION COMPLÈTE")
    print("=" * 80)
    
    base = Path(".")
    results = []
    
    # 1. Code principale
    print("\n📌 CODE PRINCIPAL")
    results.append(check_file("flask_app.py", "Flask Application"))
    results.append(check_file("storage.py", "SQLite Storage"))
    
    # 2. Module tester
    print("\n📦 MODULE TESTER")
    results.append(check_directory("tester", "Dossier tester/"))
    results.append(check_file("tester/__init__.py", "  tester/__init__.py"))
    results.append(check_file("tester/client.py", "  tester/client.py (HTTP Wrapper)"))
    results.append(check_file("tester/tests.py", "  tester/tests.py (6 Tests)"))
    results.append(check_file("tester/runner.py", "  tester/runner.py (Orchestration)"))
    
    # 3. Templates
    print("\n🎨 TEMPLATES")
    results.append(check_directory("templates", "Dossier templates/"))
    results.append(check_file("templates/dashboard.html", "  templates/dashboard.html"))
    results.append(check_file("templates/consignes.html", "  templates/consignes.html (legacy)"))
    
    # 4. Configuration
    print("\n⚙️  CONFIGURATION")
    results.append(check_file("requirements.txt", "requirements.txt (Dépendances)"))
    results.append(check_file(".env.example", ".env.example (Template)"))
    results.append(check_file(".gitignore", ".gitignore (Sécurité)"))
    results.append(check_file("pythonanywhere_wsgi_config.py", "pythonanywhere_wsgi_config.py"))
    
    # 5. Documentation
    print("\n📚 DOCUMENTATION")
    results.append(check_file("LISEZMOI_D_ABORD.txt", "LISEZMOI_D_ABORD.txt (START HERE)"))
    results.append(check_file("QUICKSTART.md", "QUICKSTART.md (5 min guide)"))
    results.append(check_file("README_SOLUTION.md", "README_SOLUTION.md (Overview)"))
    results.append(check_file("SOLUTION_SUMMARY.md", "SOLUTION_SUMMARY.md (Résumé)"))
    results.append(check_file("DEPLOYMENT.md", "DEPLOYMENT.md (PythonAnywhere)"))
    results.append(check_file("API_CHOICE.md", "API_CHOICE.md (API Documentation)"))
    
    # 6. Outils
    print("\n🛠️  OUTILS")
    results.append(check_file("test_config.py", "test_config.py (Validation local)"))
    results.append(check_file("manual_test.py", "manual_test.py (Test manuel)"))
    
    # 7. CI/CD
    print("\n🚀 CI/CD")
    results.append(check_directory(".github", "Dossier .github/"))
    results.append(check_directory(".github/workflows", "  .github/workflows/"))
    results.append(check_file(".github/workflows/deploy-pythonanywhere.yml", "  deploy-pythonanywhere.yml"))
    
    # Résumé
    print("\n" + "=" * 80)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"📊 RÉSULTAT : {passed}/{total} ({percentage:.0f}%)")
    print("=" * 80)
    
    if passed == total:
        print("✅ EXCELLENT ! Tous les fichiers sont en place !")
        print("\n🎯 Prochaines étapes :")
        print("   1. Lire LISEZMOI_D_ABORD.txt")
        print("   2. Lire QUICKSTART.md")
        print("   3. Configurer .env avec IPSTACK_API_KEY")
        print("   4. python test_config.py")
        print("   5. python flask_app.py")
        return 0
    else:
        missing = total - passed
        print(f"⚠️  {missing} fichier(s) manquant(s)")
        print("\nVérifiez la sortie ci-dessus pour les fichiers ❌ ")
        return 1

if __name__ == "__main__":
    sys.exit(main())
