#region Imports
import random
import time
import logging
from abc import ABC, abstractmethod
#endregion

#region Logger
## @brief Logger pour le module sensors
logger = logging.getLogger(__name__)
#endregion

#region Interfaces
class CSensorDriver(ABC):
    """!
    @brief Classe de base abstraite pour tous les pilotes de capteurs.

    Chaque pilote est une classe interchangeable, enregistrée dans
    SENSOR_DRIVER_REGISTRY et sélectionnée par la configuration du banc.
    """

    def __init__(self, bus, addr: int):
        """!
        @brief Constructeur d'initialisation.
        @param bus Objet bus I2C.
        @param addr Adresse du composant.
        """
        ## @brief Référence vers le bus de communication
        self.bus = bus
        ## @brief Adresse I2C du capteur
        self.addr = addr

    @abstractmethod
    def ReadValue(self, **kwargs):
        """!
        @brief Lit et retourne la valeur du capteur.
        @return Valeur lue ou None en cas d'erreur.
        """
        pass
#endregion

#region Implémentations Drivers
class CDriverAht10(CSensorDriver):
    """!
    @brief Pilote pour le capteur de température et d'humidité AHT10.
    """

    def __init__(self, bus, addr: int):
        super().__init__(bus, addr)
        try:
            self.bus.write_byte(self.addr, 0xBA)
            time.sleep(0.02)
            self.bus.write_i2c_block_data(self.addr, 0xE1, [0x08, 0x00])
            time.sleep(0.05)
            logger.debug("AHT10 @%s initialisé.", hex(addr))
        except Exception as exc:
            logger.error("Erreur init AHT10 @%s : %s", hex(addr), exc)

    def _ReadRawData(self) -> list:
        """!
        @brief Déclenche une mesure et retourne les octets bruts.
        @return Liste des octets lus.
        """
        self.bus.write_i2c_block_data(self.addr, 0xAC, [0x33, 0x00])
        time.sleep(0.08)
        return self.bus.read_i2c_block_data(self.addr, 0x00, 6)

    def ReadValue(self, channel: str = 'hum') -> float:
        """!
        @brief Lit une valeur du capteur AHT10.
        @param channel 'hum' pour l'humidité ou 'temp' pour la température.
        @return Valeur flottante ou None.
        """
        try:
            rawData = self._ReadRawData()
            if channel == 'hum':
                humRaw = (rawData[1] << 12) | (rawData[2] << 4) | (rawData[3] >> 4)
                return round((humRaw / 1_048_576.0) * 100, 2)

            tempRaw = ((rawData[3] & 0x0F) << 16) | (rawData[4] << 8) | rawData[5]
            return round((tempRaw / 1_048_576.0) * 200 - 50, 2)
        except Exception as exc:
            logger.warning("Erreur lecture AHT10 @%s : %s", hex(self.addr), exc)
            return None

class CDriverTmp102(CSensorDriver):
    """!
    @brief Pilote pour le capteur de température de précision TMP102.
    """

    def ReadValue(self, **_) -> float:
        """!
        @brief Lit le registre de température sur 12 bits.
        @return Température en degrés Celsius ou None.
        """
        try:
            rawWord = self.bus.read_word_data(self.addr, 0x00)
            rawWord = ((rawWord << 8) & 0xFF00) | (rawWord >> 8)
            tempRaw = rawWord >> 4
            if tempRaw & 0x800:
                tempRaw -= 4096
            return round(tempRaw * 0.0625, 2)
        except Exception as exc:
            logger.warning("Erreur lecture TMP102 @%s : %s", hex(self.addr), exc)
            return None

class CDriverEmc2101(CSensorDriver):
    """!
    @brief Pilote pour la température interne du contrôleur EMC2101.
    """

    def ReadValue(self, **_) -> float:
        """!
        @brief Retourne la température interne (registre 0x00).
        @return Température en degrés Celsius ou None.
        """
        try:
            tempRaw = self.bus.read_byte_data(self.addr, 0x00)
            if tempRaw > 127:
                tempRaw -= 256
            return float(tempRaw)
        except Exception as exc:
            logger.warning("Erreur lecture EMC2101 @%s : %s", hex(self.addr), exc)
            return None

class CDriverSimule(CSensorDriver):
    """!
    @brief Pilote de test pour retourner des valeurs simulées.
    """

    def ReadValue(self, channel: str = None) -> float:
        """!
        @brief Retourne des valeurs factices.
        @param channel Canal de mesure souhaité.
        @return Valeur simulée.
        """
        if channel == 'hum':
            return round(random.uniform(40.0, 60.0), 2)
        return round(random.uniform(20.0, 25.0), 2)
#endregion

#region Registre
## @brief Dictionnaire regroupant l'ensemble des drivers de capteurs.
#  Pour ajouter un capteur : créer une classe héritant de CSensorDriver puis
#  l'enregistrer ici sous le nom utilisé dans le champ 'driver' de la config.
SENSOR_DRIVER_REGISTRY: dict = {
    'AHT10':   CDriverAht10,
    'TMP102':  CDriverTmp102,
    'EMC2101': CDriverEmc2101,
    'SIMULE':  CDriverSimule,
}
#endregion
