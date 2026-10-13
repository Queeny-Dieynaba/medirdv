from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import RendezVous, Patient, Medecin, Specialite

app = FastAPI(
    title="API MediRDV - Clinique Les Baobabs",
    description="API de gestion et d'analyse des rendez-vous médicaux[cite: 1, 2].",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la Clinique Les Baobabs[cite: 1, 2]"}

@app.get("/rendez-vous/")
def lister_rendez_vous(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rdvs = db.query(RendezVous).offset(skip).limit(limit).all()
    return rdvs

@app.get("/patients/")
def lister_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/medecins/")
def lister_medecins(db: Session = Depends(get_db)):
    medecins = db.query(Medecin).all()
    return medecins

@app.get("/specialites/")
def lister_specialites(db: Session = Depends(get_db)):
    specialites = db.query(Specialite).all()
    return specialites