#region Imports
import logging
from dataclasses import dataclass
from typing import Optional
from unittest.mock import MagicMock

import pigpio
#endregion

#region Logger
## @brief Logger du module actuators
logger = logging.getLogger(__name__)
#endregion

#region Classes de Configuration et Exceptions
@dataclass
class CActuatorConfig:
    """!
    @brief Représente la configuration d'un actionneur.
    """
    title:         str
    name:          str
    pin:           int
    pwmFrequency:  int
    units:         str = ''
    minVal:        int = 0
    maxVal:        int = 255
    address:       Optional[int] = None

    @classmethod
    def FromDict(cls, data: dict) -> "CActuatorConfig":
        """!
        @brief Construit un objet de configuration à partir d'un dictionnaire.
        @param data Dictionnaire contenant les paramètres.
        @return CActuatorConfig
        """
        return cls(
            title        = data["title"],
            name         = data["name"],
            pin          = data["pin"],
            pwmFrequency = data["pwm_frequency"],
            units        = data.get("units", ''),
            minVal       = data.get("min", 0),
            maxVal       = data.get("max", 255),
            address      = data.get("address"),
        )

class CPigpioNotConnectedError(RuntimeError):
    """! @brief Exception levée quand pigpiod n'est pas joignable. """
    pass

class CPinNotFoundError(KeyError):
    """! @brief Exception levée quand le pin demandé n'existe pas. """
    pass
#endregion

#region Gestionnaire Actionneurs
class CActuatorManager:
    """!
    @brief Gestionnaire des actionneurs (moteurs, chauffages, LEDs) via GPIO en PWM.
    """

    def __init__(self, actuatorsConfig: list):
        """!
        @brief Initialise la connexion au démon pigpio et charge la configuration.
        @param actuatorsConfig Liste des dictionnaires de configuration des actionneurs.
        """
        ## @brief Interface de communication avec la librairie pigpio
        self.piClient = pigpio.pi()

        if not self.piClient.connected:
            logger.info("pigpio non connecté : passage en mode simulation")
            self.piClient = MagicMock()
            self.piClient.connected = True
            self.piClient.read_value = 1

        ## @brief Dictionnaire des actionneurs indexé par PIN
        self._actuators: dict = {}

        self._CheckConnected()
        self._LoadConfig(actuatorsConfig)

    def _CheckConnected(self) -> None:
        """!
        @brief Vérifie la connexion matérielle.
        @raises CPigpioNotConnectedError Si non connecté.
        """
        if not self.piClient.connected:
            raise CPigpioNotConnectedError("Impossible de se connecter à pigpiod.")
        logger.info("Connexion à pigpio établie.")

    def _LoadConfig(self, actuatorsConfig: list) -> None:
        """!
        @brief Charge les configurations d'actionneurs fournies.
        @param actuatorsConfig Liste des dictionnaires de configuration.
        """
        for rawConfig in actuatorsConfig:
            actuatorDef = CActuatorConfig.FromDict(rawConfig)
            self._actuators[actuatorDef.pin] = actuatorDef
            self.piClient.set_PWM_frequency(actuatorDef.pin, actuatorDef.pwmFrequency)
            self.piClient.set_PWM_dutycycle(actuatorDef.pin, 0)
            logger.debug(f"Configuré : {actuatorDef.title} (pin {actuatorDef.pin})")
        logger.info(f"{len(self._actuators)} actionneur(s) configuré(s).")

    def GetActuatorsInfo(self) -> list:
        """!
        @brief Retourne la liste des actionneurs configurés.
        @return list de CActuatorConfig
        """
        return list(self._actuators.values())

    def SetPin(self, pinTarget: int, powerValue: int) -> None:
        """!
        @brief Applique un rapport cyclique PWM sur un pin.
        @param pinTarget Numéro GPIO BCM.
        @param powerValue Puissance souhaitée.
        """
        self._CheckConnected()
        actuatorObj = self._GetActuator(pinTarget)

        clampedValue = max(actuatorObj.minVal, min(actuatorObj.maxVal, powerValue))
        if clampedValue != powerValue:
            logger.warning("Valeur %d hors plage pour %s → bornée à %d.", powerValue, actuatorObj.title, clampedValue)

        self.piClient.set_PWM_dutycycle(pinTarget, clampedValue)

    def GetPinValue(self, pinTarget: int) -> int:
        """!
        @brief Retourne la valeur PWM actuelle (0-255) du pin.
        @param pinTarget Numéro GPIO.
        @return int Valeur PWM.
        """
        self._CheckConnected()
        self._GetActuator(pinTarget)

        try:
            return int(self.piClient.get_PWM_dutycycle(pinTarget))
        except Exception as exc:
            raise RuntimeError(f"Impossible de lire la valeur du pin {pinTarget}.") from exc

    def Cleanup(self) -> None:
        """!
        @brief Éteint tous les actionneurs et ferme la connexion.
        """
        if not self.piClient.connected:
            return
        logger.info("Arrêt des actionneurs...")
        for actuatorObj in self._actuators.values():
            self.piClient.set_PWM_dutycycle(actuatorObj.pin, 0)
        self.piClient.stop()
        logger.info("Connexion pigpio fermée.")

    def __enter__(self) -> "CActuatorManager":
        return self

    def __exit__(self, *_) -> None:
        self.Cleanup()

    def _GetActuator(self, pinTarget: int) -> CActuatorConfig:
        """!
        @brief Récupère l'objet configuration d'un actionneur selon son PIN.
        @param pinTarget Numéro de broche.
        @return CActuatorConfig
        """
        try:
            return self._actuators[pinTarget]
        except KeyError:
            raise CPinNotFoundError(f"Pin {pinTarget} introuvable.")
#endregion
