from flask import Flask, render_template, jsonify, request, redirect, url_for
from tester.runner import TestRunner
from storage import TestStorage
import os
import logging
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "test-secret-key-change-in-production"

# Configuration
API_KEY = os.getenv("IPSTACK_API_KEY", "your_api_key_here")
BASE_URL = os.getenv("IPSTACK_BASE_URL", "http://api.ipstack.com")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def consignes():
    """Page d'accueil"""
    return redirect(url_for('dashboard'))

@app.get("/dashboard")
def dashboard():
    """Affiche le dashboard avec les résultats"""
    storage = TestStorage()
    latest_run = storage.get_latest_run()
    stats = storage.get_statistics()
    
    return render_template('dashboard.html', latest_run=latest_run, stats=stats)

@app.get("/history")
def history():
    """Affiche l'historique complet des tests"""
    try:
        storage = TestStorage()
        runs = storage.get_all_runs(limit=100)  # Derniers 100 runs
        stats = storage.get_statistics()
        
        # Inverser pour afficher les anciens en premier, nouveaux à la fin
        runs_reversed = list(reversed(runs))
        
        # Données pour les graphiques
        latency_chart_data = {
            "labels": [f"Run {len(runs_reversed)-i}" for i in range(len(runs_reversed))],
            "avg": [run.get("summary", {}).get("latency_ms_avg", 0) for run in runs_reversed],
            "p95": [run.get("summary", {}).get("latency_ms_p95", 0) for run in runs_reversed]
        }
        
        success_chart_data = {
            "labels": [f"Run {len(runs_reversed)-i}" for i in range(len(runs_reversed))],
            "rates": [run.get("summary", {}).get("pass_rate", 0) * 100 for run in runs_reversed]
        }
        
        return render_template(
            'history.html', 
            runs=runs,  # Garder l'ordre original (plus récent en premier) pour le timeline
            stats=stats,
            latency_chart_data=json.dumps(latency_chart_data),
            success_chart_data=json.dumps(success_chart_data)
        )
    except Exception as e:
        logger.error(f"Erreur chargement historique: {e}")
        return render_template('history.html', runs=[], stats={}, latency_chart_data=json.dumps({"labels": [], "avg": [], "p95": []}), success_chart_data=json.dumps({"labels": [], "rates": []})), 500

@app.get("/run")
def run_tests():
    """Déclenche l'exécution des tests et redirige vers le dashboard"""
    try:
        logger.info("=== Démarrage exécution tests ===")
        
        runner = TestRunner(base_url=BASE_URL)
        report = runner.run(api_key=API_KEY)
        
        # Sauvegarder le rapport
        storage = TestStorage()
        run_id = storage.save_run(report)
        
        logger.info(f"✅ Tests complétés et sauvegardés (id={run_id})")
        
        # Rediriger vers le dashboard pour afficher les résultats
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution: {e}")
        return redirect(url_for('dashboard'))

@app.get("/api/run")
def api_run_tests():
    """API JSON pour exécuter les tests (usage programmatique)"""
    try:
        runner = TestRunner(base_url=BASE_URL)
        report = runner.run(api_key=API_KEY)
        
        storage = TestStorage()
        run_id = storage.save_run(report)
        
        return jsonify({
            "status": "success",
            "message": "Tests exécutés avec succès",
            "run_id": run_id,
            "report": report
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.get("/health")
def health_check():
    """Endpoint de santé - vérifie si le service fonctionne"""
    try:
        storage = TestStorage()
        latest_run = storage.get_latest_run()
        
        if latest_run:
            last_run_time = latest_run.get("timestamp", "")
            pass_rate = latest_run.get("summary", {}).get("pass_rate", 0)
            
            status = "healthy" if pass_rate >= 0.8 else "degraded"
            
            return jsonify({
                "status": status,
                "api": "IPStack Tests",
                "last_run": last_run_time,
                "pass_rate": pass_rate,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "no_data",
                "api": "IPStack Tests",
                "message": "Aucun test exécuté pour le moment",
                "timestamp": datetime.now().isoformat()
            }), 202
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.get("/api/runs")
def get_runs():
    """API pour récupérer l'historique des runs (JSON)"""
    try:
        limit = request.args.get("limit", 10, type=int)
        storage = TestStorage()
        runs = storage.get_all_runs(limit=limit)
        
        return jsonify({
            "status": "success",
            "count": len(runs),
            "runs": runs
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.get("/api/statistics")
def get_statistics():
    """API pour récupérer les statistiques"""
    try:
        storage = TestStorage()
        stats = storage.get_statistics()
        
        return jsonify({
            "status": "success",
            "statistics": stats
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Gestion erreur 404"""
    return jsonify({
        "status": "error",
        "message": "Route non trouvée",
        "available_routes": {
            "GET /": "Redirige vers le dashboard",
            "GET /dashboard": "Affiche le dashboard",
            "GET /history": "Affiche l'historique",
            "GET /run": "Exécute les tests",
            "GET /health": "Vérifie l'état de santé",
            "GET /api/runs": "Récupère l'historique (JSON)",
            "GET /api/statistics": "Récupère les statistiques (JSON)"
        }
    }), 404

if __name__ == "__main__":
    # Utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
