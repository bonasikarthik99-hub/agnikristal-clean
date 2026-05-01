from rdkit import Chem
from rdkit.Chem import Draw


def show_molecule(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        print("Invalid SMILES")
        return

    img = Draw.MolToImage(mol, size=(400,400))
    img.show()


def show_pair(smiles1, smiles2):

    mol1 = Chem.MolFromSmiles(smiles1)
    mol2 = Chem.MolFromSmiles(smiles2)

    if mol1 is None or mol2 is None:
        print("Invalid SMILES")
        return

    img = Draw.MolsToGridImage([mol1, mol2], molsPerRow=2)
    img.show()