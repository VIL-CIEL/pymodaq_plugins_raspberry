# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/) :
`MAJEUR.MINEUR.CORRECTIF`.

- **MAJEUR** : refonte ou rupture de compatibilité
- **MINEUR** : nouvelle fonctionnalité
- **CORRECTIF** : correction de bug ou ajustement mineur

La version courante est également disponible dans [`version.json`](version.json).

## [5.1.0] - 2026-06-10

Fusion des plugins `pymodaq_plugins_raspberrypi3` et `pymodaq_plugins_raspberrypizero`
dans `pymodaq_plugins_raspberry` — **Sprint 1 : infrastructure et refonte du serveur**.

### Ajouté
- `version.json` à la racine : version du produit fusionné (SemVer).
- `CHANGELOG.md` et `CONTRIBUTING.md` (stratégie de branches/tags, processus de version).
- Serveur Raspberry refondu dans `src_raspberry/` selon une topologie en couches,
  chaque maillon étant une **classe interchangeable** derrière une interface :
  - `ITransport` / `ZmqServer` — communication avec le client PyMoDAQ (ZeroMQ) ;
  - `IRequestHandler` / `JsonRequestHandler` — décodage et routage des requêtes JSON,
    sans aucun accès matériel ;
  - `IHardwareBackend` / `HardwareBackend` — communication avec les capteurs et actionneurs ;
  - `main.py` — boucle principale qui assemble les trois couches.

### Modifié
- La gestion des requêtes et la communication matérielle, auparavant mélangées dans
  `CProtocolHandler`, sont désormais deux entités distinctes (`JsonRequestHandler`
  d'un côté, `HardwareBackend` de l'autre).
- Le transport ZeroMQ est isolé de la logique de framing/décodage des messages.
- Comportement fonctionnel identique au serveur Raspberry Pi 3 d'origine
  (la fusion des bancs Pi 3 / Pi Zero arrive au Sprint 2).
