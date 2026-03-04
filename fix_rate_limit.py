#!/usr/bin/env python3
"""
Problème : Erreur 429 Too Many Requests de IPStack
Solution : Attendre et relancer

IPStack gratuit = 10 appels/minute = 1 appel tous les 6 secondes
"""

import time
import sys

def main():
    print("=" * 70)
    print("⚠️  RATE LIMIT IPSTACK - GUIDE SOLUTION")
    print("=" * 70)
    
    print("\n📊 VOTRE LIMITATION")
    print("-" * 70)
    print("API IPStack gratuite : 10 requêtes par minute")
    print("  → 1 requête maximum toutes les 6 secondes")
    print("  → 6 tests × 1 req chacun = 6-10+ requêtes par run")
    print("")
    print("⚠️  Vous avez probablement cliqué 'Exécuter' trop vite")
    print("    Cela a versé >10 requêtes en quelques secondes")
    print("    IPStack a répondu : 429 Too Many Requests")
    
    print("\n✅ SOLUTION 1 : ATTENDRE (Le plus simple)")
    print("-" * 70)
    print("IPStack réinitialise la limite chaque minute")
    print("")
    print("Attendez 1 minute complète, puis :")
    print("  1. Actualiser la page (F5 ou Ctrl+R)")
    print("  2. Cliquer 'Exécuter les tests'")
    print("  3. ATTENDRE 10-15 secondes pendant l'exécution")
    print("")
    print("Puis, pour les exécutions suivantes :")
    print("  → Attendre 60 secondes minimum entre les exécutions")
    
    print("\n⏱️  TIMING RECOMMANDÉ")
    print("-" * 70)
    print("Exécution 1 : 10:00:00 ✅")
    print("Attendre    : 60 secondes")
    print("Exécution 2 : 10:01:00 ✅")
    print("Attendre    : 60 secondes")
    print("Exécution 3 : 10:02:00 ✅")
    
    print("\n📋 CONFIGURATIONS")
    print("-" * 70)
    print("")
    print("LOCAL (Développement)")
    print("  • testé/tests.py : TEST_DELAY = 1 seconde entre tests")
    print("  • 6 tests = ~6 secondes total")
    print("  • 1 appel/6 secondes respecte le limit")
    print("")
    print("PYTHONANYWHERE (Production)")
    print("  • Tâche planifiée TOUTES LES 5+ MINUTES")
    print("  • JAMAIS exécuter plus souvent")
    print("  • La limite se réinitialise chaque minute")
    
    print("\n🔧 CONFIGURATION ACTUALISÉE")
    print("-" * 70)
    print("Le code a été mis à jour avec :")
    print("  ✅ Délais automatiques entre les tests")
    print("  ✅ Gestion meilleure des erreurs 429")
    print("  ✅ Vérification des latences valides")
    
    print("\n🚀 PROCHAINES ÉTAPES")
    print("-" * 70)
    print("")
    print("1. ATTENDRE 1 MINUTE")
    print("   (C'est important ! IPStack reset chaque minute)")
    print("")
    print("2. RAFRAICHIR LA PAGE")
    print("   http://localhost:5000/dashboard")
    print("   Touche : F5 ou Ctrl+R")
    print("")
    print("3. CLIQUER BOUTON")
    print("   '▶️ Exécuter les tests maintenant'")
    print("")
    print("4. ATTENDRE 10-15 SECONDES")
    print("   Laissez le code s'exécuter")
    print("   (6 tests × 1s délai chacun)")
    print("")
    print("5. VÉRIFIER RÉSULTATS")
    print("   Le dashboard doit afficher les résultats")
    
    print("\n💡 CONSEIL")
    print("-" * 70)
    print("Si vous testez localement plusieurs fois :")
    print("  → Attendez AU MOINS 1 minute entre les exécutions")
    print("  → Ou utilisez une clé API payante IPStack (pas gratuit)")
    print("")
    print("Les tests planifiés sur PythonAnywhere (5 min min)")
    print("  → Devraient fonctionner sans problème rate limit")
    
    # Optionnel : countdown timer
    response = input("\nFaire un compte à rebours de 60 secondes ? (y/n): ").lower().strip()
    if response == 'y':
        print("\n⏳ Attendre 60 secondes...")
        for i in range(60, 0, -1):
            if i % 10 == 0 or i <= 5:
                print(f"   {i} secondes restantes...", end='\r')
            time.sleep(1)
        print("✅ 60 secondes écoulées ! Vous pouvez relancer les tests maintenant.")
        print("   Allez à http://localhost:5000/dashboard et cliquez 'Exécuter'")
    
    print("\n" + "=" * 70)
    print("Bonne chance ! 🚀")
    print("=" * 70)

if __name__ == "__main__":
    main()
