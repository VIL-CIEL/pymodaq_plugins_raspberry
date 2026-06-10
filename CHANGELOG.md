# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/) :
`MAJEUR.MINEUR.CORRECTIF`.

- **MAJEUR** : refonte ou rupture de compatibilité
- **MINEUR** : nouvelle fonctionnalité
- **CORRECTIF** : correction de bug ou ajustement mineur

La version courante est également disponible dans [`version.json`](version.json).

## [5.4.2] - 2026-06-10

### Modifié
- `README.rst` réécrit du point de vue de l'utilisateur du plugin (contrôle d'un
  dispositif expérimental via un Raspberry). Mise en avant des trois axes
  d'adaptabilité : communication PyMoDAQ ⇄ Raspberry, communication
  Raspberry ⇄ composants, et ajout de nouvelles requêtes JSON des deux côtés.

## [5.4.1] - 2026-06-10

### Corrigé
- `CONTRIBUTING.md` : convention de tags alignée sur l'historique du dépôt
  (`5.0.0`, `5.0.1`) — les tags de production sont au format `MAJEUR.MINEUR.CORRECTIF`
  sans préfixe `v`.

## [5.4.0] - 2026-06-10

Fusion des plugins `pymodaq_plugins_raspberrypi3` et `pymodaq_plugins_raspberrypizero` —
**Sprint 4 : finitions et documentation** (première version « production » du plugin fusionné).

### Ajouté
- Documentation du plugin fusionné dans `README.rst` : liste des instruments
  (`MoveRasp`, `ViewRasp`, `picamera`) et description du serveur Raspberry
  (`src_raspberry/`).

### Modifié
- `README.rst` : mise à jour des auteurs, de la version PyMoDAQ requise (>= 5) et
  des cartes testées (Raspberry Pi 3 et Pi Zero).

### Vérifié
- Conformité à `tests/test_plugin_package_structure.py` (conventions de nommage et
  méthodes obligatoires des plugins `DAQ_Move_MoveRasp` et `DAQ_0DViewer_ViewRasp`) ;
  aucune modification du test n'a été nécessaire.

## [5.3.0] - 2026-06-10

Fusion des plugins `pymodaq_plugins_raspberrypi3` et `pymodaq_plugins_raspberrypizero` —
**Sprint 3 : intégration du client PyMoDAQ**.

### Ajouté
- `hardware/Link_PMQ.py` : client `ZMQLink` (lien ZeroMQ DEALER vers le serveur Raspberry).
- `hardware/Config_Components.py` : lecture des composants (actionneurs/détecteurs)
  depuis le fichier de configuration TOML.
- `daq_move_plugins/daq_move_MoveRasp.py` : plugin actionneur `DAQ_Move_MoveRasp`.
- `daq_viewer_plugins/plugins_0D/daq_0Dviewer_ViewRasp.py` : plugin détecteur
  `DAQ_0DViewer_ViewRasp`.

### Modifié
- `resources/config_template.toml` : section de configuration unifiée `[Raspberry]`
  (remplace les sections spécifiques `[RaspPi3]` / `[RaspPiZero]` des plugins d'origine).
- `pyproject.toml` : ajout de la dépendance `pyzmq` (requise par `ZMQLink`).
- Le plugin `DAQ_2DViewer_PiCamera` existant n'est pas modifié.

### Corrigé
- Remplacement des f-strings à guillemets imbriqués identiques (`f"{d["k"]}"`),
  valides seulement en Python 3.12+, par une forme compatible Python 3.8+.

## [5.2.0] - 2026-06-10

Fusion des plugins `pymodaq_plugins_raspberrypi3` et `pymodaq_plugins_raspberrypizero` —
**Sprint 2 : fusion des bancs de test (capteurs et actionneurs pilotés par config)**.

### Ajouté
- Pilote de capteur `PT-100` (sonde de température via CAN ADS1115), enregistré
  dans `SENSOR_DRIVER_REGISTRY` (import de la dépendance Adafruit isolé localement).
- Pilotes d'actionneurs **interchangeables** derrière l'interface `CActuatorDriver`,
  sélectionnés par le champ `driver` de la configuration, et enregistrés dans
  `ACTUATOR_DRIVER_REGISTRY` :
  - `PWM` — pilotage en rapport cyclique (ex-banc Raspberry Pi 3) ;
  - `DIGITAL` — pilotage tout-ou-rien (ex-banc Raspberry Pi Zero).
- `config_examples/config_pizero.py` : configuration d'exemple d'un banc tout-ou-rien
  avec sonde PT100.

### Modifié
- `CActuatorManager` instancie désormais le pilote adapté à chaque actionneur
  (au lieu d'un pilotage PWM codé en dur), permettant de mélanger des modes de
  pilotage différents sur un même banc.
- `CActuatorConfig` accepte un champ `driver` (défaut `PWM`) ; `pwm_frequency`
  devient optionnel (inutile pour les actionneurs tout-ou-rien).
- `config.py` documente le choix du pilote par actionneur.

### Supprimé
- Le moniteur de sécurité (`safety_monitor.py`) des plugins d'origine n'est pas
  repris : il lisait des constantes de configuration inexistantes et n'était
  jamais démarré par le `main`.

### Corrigé
- La fonction morte `build_sensor_map` (références non importées dans l'ancien
  `connexion.py`) n'est pas reprise ; la construction de la cartographie des
  capteurs est unifiée dans `HardwareBackend`.
- L'indentation cassée et la perte de `pwm_frequency` de l'ancien `actuators.py`
  côté Pi Zero sont résolues par le nouveau modèle de pilotes d'actionneurs.

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
