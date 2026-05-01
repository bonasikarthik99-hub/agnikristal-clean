from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Lipinski


def calculate_descriptors(smiles):
    """
    Calculate molecular descriptors for AgniKristal.
    Compatible with AgniKristal 1.x descriptor logic.
    """

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise ValueError("Invalid SMILES string")

    descriptors = {}

    # Basic physicochemical properties
    descriptors["MolecularWeight"] = Descriptors.MolWt(mol)
    descriptors["LogP"] = Descriptors.MolLogP(mol)
    descriptors["TPSA"] = rdMolDescriptors.CalcTPSA(mol)

    # Hydrogen bonding
    descriptors["HBD"] = Lipinski.NumHDonors(mol)
    descriptors["HBA"] = Lipinski.NumHAcceptors(mol)

    # Flexibility
    descriptors["RotatableBonds"] = Lipinski.NumRotatableBonds(mol)

    # Aromaticity / ring systems
    descriptors["AromaticRings"] = rdMolDescriptors.CalcNumAromaticRings(mol)
    descriptors["RingCount"] = rdMolDescriptors.CalcNumRings(mol)

    # Size descriptor
    descriptors["HeavyAtoms"] = mol.GetNumHeavyAtoms()

    return descriptors


def estimate_api_polarity(logP, TPSA):
    """
    Estimate API polarity index used in AgniKristal solvent matching.
    """

    polarity = (TPSA / 100) + (3 - logP)

    return round(polarity, 3)