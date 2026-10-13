-- ----------------------------------------------------------------------------
-- SECTION 1 : CREATION DU SCHEMA ET DES TABLES
-- ----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS medirdv
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE medirdv; 

DROP TABLE IF EXISTS rendez_vous;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS medecin;
DROP TABLE IF EXISTS specialite;

CREATE TABLE specialite (
    id_specialite INT AUTO_INCREMENT PRIMARY KEY,
    nom_specialite VARCHAR(100) NOT NULL UNIQUE,
    duree_minutes INT DEFAULT 20
) ENGINE=InnoDB;

CREATE TABLE medecin (
    id_medecin VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    id_specialite INT NOT NULL,
    FOREIGN KEY (id_specialite) REFERENCES specialite(id_specialite) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE patient (
    id_patient VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    date_naissance DATE,
    sexe CHAR(1),
    telephone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE rendez_vous (
    id_rdv INT AUTO_INCREMENT PRIMARY KEY,
    id_rdv_code VARCHAR(20) UNIQUE,
    id_patient VARCHAR(20) NOT NULL,
    id_medecin VARCHAR(20) NOT NULL,
    date_prise DATETIME NOT NULL,
    date_rdv DATETIME NOT NULL,
    statut ENUM('Honore', 'Absent', 'Annule', 'Planifie', 'Confirme') NOT NULL,
    confirmation_sms TINYINT(1) DEFAULT 0,
    motif_annulation VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (id_patient) REFERENCES patient(id_patient) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_medecin) REFERENCES medecin(id_medecin) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Index pour optimiser la vitesse d'execution des calculs d'indicateur
CREATE INDEX idx_date_rdv ON rendez_vous(date_rdv);
CREATE INDEX idx_statut ON rendez_vous(statut);


-- ----------------------------------------------------------------------------
-- SECTION 2 : CHARGEMENT DES DONNEES (Géré automatiquement depuis Jupyter)
-- ----------------------------------------------------------------------------
-- Note : L'injection des données (patients et rendez-vous) est directement 
-- pilotée par le Notebook Jupyter via SQLAlchemy pour s'affranchir des restrictions 
-- de sécurité du serveur MySQL (secure-file-priv).


-- ----------------------------------------------------------------------------
-- SECTION 3 : REQUETES DES INDICATEURS ET REGLES DE GESTION (DATE PIVOT : 28/09/2026)
-- ----------------------------------------------------------------------------

-- 1. RG-09 : TAUX D'ABSENCE HISTORIQUE (Absents / (Honores + Absents) * 100)
SELECT 
    SUM(CASE WHEN statut = 'Absent' THEN 1 ELSE 0 END) AS nb_absents,
    SUM(CASE WHEN statut = 'Honore' THEN 1 ELSE 0 END) AS nb_honores,
    SUM(CASE WHEN statut IN ('Honore', 'Absent') THEN 1 ELSE 0 END) AS total_evalues,
    ROUND(
        SUM(CASE WHEN statut = 'Absent' THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN statut IN ('Honore', 'Absent') THEN 1 ELSE 0 END), 0), 
        2
    ) AS taux_absence_pct
FROM rendez_vous
WHERE date_rdv <= '2026-09-28';


-- 2. TAUX D'OCCUPATION / HONORÉS
SELECT 
    SUM(CASE WHEN statut = 'Honore' THEN 1 ELSE 0 END) AS nb_honores,
    COUNT(*) AS total_rdv_passes,
    ROUND(
        SUM(CASE WHEN statut = 'Honore' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS taux_occupation_pct
FROM rendez_vous
WHERE date_rdv <= '2026-09-28';


-- 3. DELAI MEDIAN D'ATTENTE (EN JOURS)
WITH DelaisRdv AS (
    SELECT 
        DATEDIFF(date_rdv, date_prise) AS delai_jours,
        ROW_NUMBER() OVER (ORDER BY DATEDIFF(date_rdv, date_prise)) AS row_num,
        COUNT(*) OVER () AS total_rows
    FROM rendez_vous
    WHERE date_rdv <= '2026-09-28'
)
SELECT 
    ROUND(AVG(delai_jours), 1) AS delai_median_jours
FROM DelaisRdv
WHERE row_num IN (FLOOR((total_rows + 1) / 2), CEIL((total_rows + 1) / 2));


-- 4. TAUX D'ANNULATION HISTORIQUE (Annules / Total RDV Passes * 100)
SELECT 
    SUM(CASE WHEN statut = 'Annule' THEN 1 ELSE 0 END) AS nb_annules,
    COUNT(*) AS total_rdv_passes,
    ROUND(
        SUM(CASE WHEN statut = 'Annule' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS taux_annulation_pct
FROM rendez_vous
WHERE date_rdv <= '2026-09-28';


-- 5. VOLUME ET TAUX D'ABSENCE PAR SPECIALITE
SELECT 
    s.nom_specialite,
    COUNT(r.id_rdv) AS total_rdv,
    SUM(CASE WHEN r.statut = 'Honore' THEN 1 ELSE 0 END) AS nb_honores,
    SUM(CASE WHEN r.statut = 'Absent' THEN 1 ELSE 0 END) AS nb_absences,
    ROUND(
        SUM(CASE WHEN r.statut = 'Absent' THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN r.statut IN ('Honore', 'Absent') THEN 1 ELSE 0 END), 0), 
        2
    ) AS taux_absence_pct
FROM rendez_vous r
JOIN medecin m ON r.id_medecin = m.id_medecin
JOIN specialite s ON m.id_specialite = s.id_specialite
WHERE r.date_rdv <= '2026-09-28'
GROUP BY s.nom_specialite
ORDER BY total_rdv DESC;



USE medirdv;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE rendez_vous;
TRUNCATE TABLE medecin;
TRUNCATE TABLE patient;
TRUNCATE TABLE specialite;
SET FOREIGN_KEY_CHECKS = 1;

USE medirdv;
ALTER TABLE patient MODIFY COLUMN sexe VARCHAR(10);
ALTER TABLE rendez_vous MODIFY COLUMN statut VARCHAR(50);
ALTER TABLE specialite ADD COLUMN couleur VARCHAR(20) NULL;