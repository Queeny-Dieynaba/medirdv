from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from api.database import Base

class Specialite(Base):
    __tablename__ = "specialite"

    id_specialite = Column(Integer, primary_key=True, autoincrement=True)
    nom_specialite = Column(String(100), unique=True, nullable=False)
    duree_minutes = Column(Integer, default=30)
    couleur = Column(String(20), nullable=True)

    medecins = relationship("Medecin", back_populates="specialite")

class Medecin(Base):
    __tablename__ = "medecin"

    id_medecin = Column(String(20), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=True)
    id_specialite = Column(Integer, ForeignKey("specialite.id_specialite"), nullable=False)

    specialite = relationship("Specialite", back_populates="medecins")
    rendez_vous = relationship("RendezVous", back_populates="medecin")

class Patient(Base):
    __tablename__ = "patient"

    id_patient = Column(String(20), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)
    sexe = Column(String(10), nullable=False)
    telephone = Column(String(20), nullable=False)

    rendez_vous = relationship("RendezVous", back_populates="patient")

class RendezVous(Base):
    __tablename__ = "rendez_vous"

    id_rdv_code = Column(String(20), primary_key=True)
    id_patient = Column(String(20), ForeignKey("patient.id_patient"), nullable=False)
    id_medecin = Column(String(20), ForeignKey("medecin.id_medecin"), nullable=False)
    date_prise = Column(Date, nullable=False)
    date_rdv = Column(DateTime, nullable=False)
    statut = Column(String(50), default="Planifie")
    confirmation_sms = Column(Integer, default=0)
    motif_annulation = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="rendez_vous")
    medecin = relationship("Medecin", back_populates="rendez_vous")