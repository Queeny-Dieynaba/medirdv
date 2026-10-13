# Jeu de données MédiRDV — dictionnaire et notice

Fichier : `rendez_vous_medirdv_brut.csv` · 2 040 lignes · 20 colonnes · encodage UTF-8 · séparateur virgule.
Données **entièrement fictives**, générées par programme (graine aléatoire 42). Aucune personne réelle.

Période couverte : rendez-vous du 1er octobre 2025 au 31 décembre 2026. Les rendez-vous postérieurs au 28 septembre 2026 sont « futurs » (statut Planifié ou Confirmé).

## Dictionnaire des colonnes

| Colonne | Type attendu | Description | Valeurs attendues |
| --- | --- | --- | --- |
| id_rdv | texte | Identifiant du rendez-vous | RDV00001 à RDV02015, unique |
| date_prise | date | Date à laquelle le rendez-vous a été pris | AAAA-MM-JJ, antérieure ou égale à date_rdv |
| date_rdv | date | Date du rendez-vous | AAAA-MM-JJ, du lundi au samedi |
| heure_rdv | heure | Heure de début | HH:MM, entre 08:00 et 18:00 |
| duree_min | entier | Durée du créneau | 15, 20 ou 30 selon la spécialité |
| specialite | catégorie | Spécialité | 9 valeurs (voir ci-dessous) |
| medecin_id | texte | Identifiant du médecin | MED001 à MED030 |
| medecin_nom | texte | Nom du médecin | « Dr Prénom Nom » |
| patient_id | texte | Identifiant du patient | PAT00001 à PAT01000 |
| patient_nom | texte | Nom du patient | |
| patient_prenom | texte | Prénom du patient | |
| sexe | catégorie | Sexe du patient | F ou M |
| date_naissance | date | Date de naissance | AAAA-MM-JJ, plausible |
| telephone | texte | Téléphone mobile | 9 chiffres commençant par 70, 75, 76, 77 ou 78 |
| quartier | catégorie | Quartier de résidence (Dakar et environs) | 16 valeurs |
| canal | catégorie | Canal de prise du rendez-vous | Téléphone, Guichet, Recommandation médecin |
| confirme | catégorie | Le patient a-t-il confirmé ? | Oui, Non |
| statut | catégorie | Statut du rendez-vous | Planifié, Confirmé, Honoré, Absent, Annulé |
| motif_annulation | catégorie | Motif si annulé, vide sinon | Patient, Médecin, Clinique, Autre |
| agent_saisie | texte | Agent d'accueil ayant saisi le rendez-vous | AGT01 à AGT08 |

Spécialités et durées : Médecine générale (15 min), Pédiatrie (20), Gynécologie-obstétrique (30), Cardiologie (30), Dermatologie (20), Ophtalmologie (20), ORL (20), Endocrinologie (30), Kinésithérapie (30).

## Effets réalistes intégrés (à retrouver par l'analyse)

- Pics de demande le lundi et le samedi, surtout le matin.
- Hausse de l'activité de juillet à septembre (saison des pluies).
- Taux d'absence global d'environ 14 %, plus élevé quand le délai de prise est long, quand le rendez-vous n'est pas confirmé, chez les 18-35 ans, l'après-midi, et pour certains patients « habitués » à manquer.
- Pédiatrie réservée aux moins de 16 ans ; gynécologie aux femmes.

## Travail attendu des étudiants

1. Charger le fichier et produire un diagnostic de qualité (types, valeurs manquantes, doublons, valeurs hors domaine).
2. Nettoyer et standardiser chaque colonne, en documentant chaque règle appliquée et le nombre de lignes touchées.
3. Vérifier les règles de gestion du cahier des charges (RG-01, RG-04, RG-05…).
4. Exporter une version propre (`rendez_vous_medirdv_propre.csv`) et un rapport de nettoyage.
5. Utiliser la version propre pour le tableau de bord, la prévision et le score d'absence.
