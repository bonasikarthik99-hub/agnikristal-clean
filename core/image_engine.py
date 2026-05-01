# ============================================
# AgniKristal 2.0 — Image Engine (Stable Version)
# ============================================

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import math


# ------------------------------
# Find closest interaction atoms
# ------------------------------
def find_hbond_atoms(mol1, mol2):
    conf1 = mol1.GetConformer()
    conf2 = mol2.GetConformer()

    min_dist = 100
    best_pair = (0, 0)

    for i in range(mol1.GetNumAtoms()):
        for j in range(mol2.GetNumAtoms()):

            pos1 = conf1.GetAtomPosition(i)
            pos2 = conf2.GetAtomPosition(j)

            dist = math.sqrt(
                (pos1.x - pos2.x) ** 2 +
                (pos1.y - pos2.y) ** 2 +
                (pos1.z - pos2.z) ** 2
            )

            if dist < min_dist:
                min_dist = dist
                best_pair = (i, j)

    return best_pair


# ------------------------------
# Generate 3D Image (Stable)
# ------------------------------
def generate_cocrystal_image(api_smiles, coformer_smiles, filename="cocrystal.png"):

    # Convert SMILES to molecules
    mol1 = Chem.AddHs(Chem.MolFromSmiles(api_smiles))
    mol2 = Chem.AddHs(Chem.MolFromSmiles(coformer_smiles))

    # Generate 3D coordinates
    AllChem.EmbedMolecule(mol1, randomSeed=42)
    AllChem.EmbedMolecule(mol2, randomSeed=24)

    AllChem.UFFOptimizeMolecule(mol1)
    AllChem.UFFOptimizeMolecule(mol2)

    # Shift second molecule slightly
    conf2 = mol2.GetConformer()
    for i in range(mol2.GetNumAtoms()):
        pos = conf2.GetAtomPosition(i)
        conf2.SetAtomPosition(i, (pos.x + 3, pos.y, pos.z))

    # Find closest interaction atoms
    atom1, atom2 = find_hbond_atoms(mol1, mol2)

    # Combine molecules
    combined = Chem.CombineMols(mol1, mol2)

    # Highlight interaction atoms (SAFE + STABLE)
    highlight_atoms = [
        atom1,
        atom2 + mol1.GetNumAtoms()
    ]

    # Draw image
    drawer = rdMolDraw2D.MolDraw2DCairo(800, 600)
    opts = drawer.drawOptions()
    opts.addAtomIndices = False

    drawer.DrawMolecule(
        combined,
        highlightAtoms=highlight_atoms
    )

    drawer.FinishDrawing()

    # Save image
    with open(filename, "wb") as f:
        f.write(drawer.GetDrawingText())

    print(f"✅ 3D Image (interaction highlighted) saved: {filename}")