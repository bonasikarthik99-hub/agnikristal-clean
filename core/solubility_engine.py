# ============================================
# AgniKristal 2.0 — R&D Solubility Engine v2
# ============================================

from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski
import numpy as np

# ------------------------------
# 1. DESCRIPTORS
# ------------------------------
def compute_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    
    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Crippen.MolLogP(mol),
        "TPSA": Descriptors.TPSA(mol),
        "HBD": Lipinski.NumHDonors(mol),
        "HBA": Lipinski.NumHAcceptors(mol),
    }

# ------------------------------
# 2. BASIC pKa ESTIMATION
# (Replace later with real predictor)
# ------------------------------
def estimate_pka(smiles):
    if "COOH" in smiles:
        return 4.5
    elif "NH2" in smiles:
        return 9.5
    return 7.0

# ------------------------------
# 3. logS MODEL (R&D STANDARD)
# ------------------------------
def estimate_logS(desc, melting_point=150):
    logP = desc["LogP"]
    logS = 0.5 - 0.01 * (melting_point - 25) - logP
    return round(logS, 3)

# ------------------------------
# 4. pH-DEPENDENT SOLUBILITY
# ------------------------------
def pH_solubility(logS, pKa, pH=7.4):
    intrinsic_S = 10**logS
    sol = intrinsic_S * (1 + 10**(pH - pKa))
    return round(np.log10(sol), 3)

# ------------------------------
# 5. HANSEN ESTIMATION
# ------------------------------
def estimate_hansen(desc):
    return {
        "dD": 16 + 0.1 * desc["LogP"],
        "dP": 8 + 0.2 * desc["TPSA"] / 100,
        "dH": 10 + desc["HBD"] * 2
    }

SOLVENTS = [
    {"name": "Water", "dD": 15.5, "dP": 16.0, "dH": 42.3},
    {"name": "Ethanol", "dD": 15.8, "dP": 8.8, "dH": 19.4},
    {"name": "DMSO", "dD": 18.4, "dP": 16.4, "dH": 10.2},
    {"name": "Acetone", "dD": 15.5, "dP": 10.4, "dH": 7.0}
]

def hansen_distance(solute, solvent):
    return np.sqrt(
        (solute["dD"] - solvent["dD"])**2 +
        (solute["dP"] - solvent["dP"])**2 +
        (solute["dH"] - solvent["dH"])**2
    )

# ------------------------------
# 6. SOLVENT SCORING (R&D)
# ------------------------------
def solvent_score_from_distance(dist):
    return np.exp(-dist / 5)

# ------------------------------
# 7. MAIN SOLUBILITY FUNCTION
# ------------------------------
def compute_solubility(smiles):
    
    desc = compute_descriptors(smiles)
    if desc is None:
        return None
    
    pKa = estimate_pka(smiles)
    
    # --- R&D Models ---
    logS_intrinsic = estimate_logS(desc)
    logS_pH = pH_solubility(logS_intrinsic, pKa)
    
    # --- Hansen + solvent scoring ---
    solute = estimate_hansen(desc)
    solvent_scores = []
    
    for s in SOLVENTS:
        dist = hansen_distance(solute, s)
        score = solvent_score_from_distance(dist)
        solvent_scores.append((s["name"], round(score, 3)))
    
    solvent_scores = sorted(solvent_scores, key=lambda x: x[1], reverse=True)
    
    # --- Confidence ---
    confidence = round(1 / (1 + abs(desc["LogP"] - 2)), 2)
    
    return {
        "logS_intrinsic": logS_intrinsic,
        "logS_pH_7_4": logS_pH,
        "top_solvents": solvent_scores[:3],
        "anti_solvents": solvent_scores[-2:],
        "confidence": confidence
    }