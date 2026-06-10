# Contribuer

## Versioning et notes de version

### Numérotation
Format obligatoire : `MAJEUR.MINEUR.CORRECTIF` (ex. `5.1.0`).

- **MAJEUR** : refonte ou rupture de compatibilité
- **MINEUR** : nouvelle fonctionnalité
- **CORRECTIF** : correction de bug ou ajustement mineur

La version courante est portée par [`version.json`](version.json) à la racine du projet.

### Fichier `CHANGELOG.md`
- Présent à la racine, mis à jour à **chaque** modification livrée.
- Une entrée par version, avec les sections : `Ajouté`, `Modifié`, `Corrigé`,
  `Supprimé`, `Sécurité`.
- Aucun merge en production sans mise à jour du `CHANGELOG.md`.

### Branches Git
- `main` : version en production
- `develop` : version en cours
- `feature/nom-court` : nouvelles fonctionnalités
- `hotfix/nom-court` : correctifs urgents

### Tags
- Tag Git obligatoire à chaque déploiement en production, préfixé par `v`
  (ex. `v5.1.0`), aligné sur `version.json`.

## Découpage du travail de fusion (sprints)

| Version | Sprint | Contenu |
|---------|--------|---------|
| 5.1.0   | Sprint 1 | Infrastructure (versioning) + refonte du serveur en couches interchangeables |
| 5.2.0   | Sprint 2 | Fusion des bancs Pi 3 / Pi Zero (registres capteurs + actionneurs, pilotage par config) |
| 5.3.0   | Sprint 3 | Intégration du client PyMoDAQ (Link_PMQ, daq_move, daq_viewer) |
| 5.4.0   | Sprint 4 | Config template fusionné, tests, documentation |
