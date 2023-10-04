from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
import numpy as np


def get_cfps(mol: Mol, radius: int = 1, nBits: int = 1024, useFeatures: bool = False,
             dtype: np.dtype = np.int8) -> np.ndarray:
    """Calculates circular (Morgan) fingerprint.
    https://rdkit.org/docs/GettingStartedInPython.html#morgan-fingerprints-circular-fingerprints

    Parameters
    ----------
    mol : rdkit.Chem.rdchem.Mol
    radius : int
        Fingerprint radius
    nBits : int
        Length of hashed fingerprint (without descriptors)
    useFeatures : bool
        To get feature fingerprints (FCFP) instead of normal ones (ECFP), defaults to False
    dtype : np.dtype
        Numpy data type for the array.

    Returns
    -------
    np.ndarray
        np array with the fingerprint
    """
    arr = np.zeros((1,), dtype)
    DataStructs.ConvertToNumpyArray(
        AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits, useFeatures=useFeatures), arr)
    return arr
