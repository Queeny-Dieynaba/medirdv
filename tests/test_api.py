# ==============================================================================
# SUITE DE TESTS AUTOMATISÉS FASTAPI - CLINIQUE LES BAOBABS
# ==============================================================================
import sys
import os

# Ajout du dossier racine au chemin d'importation Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from api.main import app

# Initialisation du client de test FastAPI
client = TestClient(app)

def test_read_root():
    """Test de la route racine de l'API."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_lister_specialites():
    """Test de récupération de la liste des spécialités."""
    response = client.get("/specialites/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_lister_medecins():
    """Test de récupération de la liste des médecins."""
    response = client.get("/medecins/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_lister_patients():
    """Test de récupération de la liste des patients avec pagination."""
    response = client.get("/patients/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 10

def test_lister_rendez_vous():
    """Test de récupération des rendez-vous."""
    response = client.get("/rendez-vous/?skip=0&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5

def test_route_inexistante():
    """Test de gestion d'erreur sur une route non définie."""
    response = client.get("/route-invalide/")
    assert response.status_code == 404