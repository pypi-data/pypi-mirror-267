"""Molecular Featurization Pipeline"""

from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys

from .utils import InvalidSMILESError


class FingerprintCalculator:
    def __init__(self, descriptor="morgan2"):
        self.descriptor = descriptor
        self.descriptors = {
            "maccs": lambda m: MACCSkeys.GenMACCSKeys(m),
            "morgan2": lambda m: AllChem.GetMorganFingerprintAsBitVect(m, 2, 2048),
            "morgan3": lambda m: AllChem.GetMorganFingerprintAsBitVect(m, 3, 2048),
            "rdkit": lambda m: Chem.RDKFingerprint(m),
        }

    def calculate_fingerprint(self, smi):
        mol = Chem.MolFromSmiles(smi)
        if mol:
            fn = self.descriptors[self.descriptor]
            return fn(mol)
        raise InvalidSMILESError
