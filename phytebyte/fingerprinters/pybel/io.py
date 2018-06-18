import logging
import pybel


class SmilesDeserializationError(Exception):
    pass


class PybelDeserializer():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def smiles_to_molecule(self, smiles: str):
        try:
            mol = pybel.readstring("smi", smiles)
        except OSError as e:
            self.logger.error(e)
            self.logger.error(f"Couldn't load {smiles}")
            raise SmilesDeserializationError()
        return mol
