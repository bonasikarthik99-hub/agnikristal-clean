# ============================================
# AgniKristal 2.0 — Direct Mode + 3D Image
# ============================================

from rdkit import Chem

# ================= CORE IMPORTS =================
from core.descriptor_engine import calculate_descriptors
from core.interaction_engine import analyze_interaction
from core.synthon_engine import analyze_synthon
from core.cocrystal_probability_engine import calculate_probability

# 🔥 NEW: image engine
from core.image_engine import generate_cocrystal_image

# 3D generator
try:
    from complex_visualizer import generate_complex
    COMPLEX_AVAILABLE = True
except:
    COMPLEX_AVAILABLE = False


# ================= HELPERS =================

def is_valid_smiles(smiles):
    return Chem.MolFromSmiles(smiles) is not None


def classify_probability(prob):
    if prob >= 75:
        return "Highly Promising Co-crystal Candidate", "Strong"
    elif prob >= 55:
        return "Moderately Promising Candidate", "Moderate"
    else:
        return "Low Probability Candidate", "Weak"


def classify_stability(prob, interaction, synthon):
    stability_raw = (0.5 * interaction) + (0.5 * synthon)

    if prob >= 70:
        stability_raw += 0.15
    elif prob >= 55:
        stability_raw += 0.08

    stability_raw = min(stability_raw, 1.0)
    stability_percent = round(stability_raw * 100, 2)

    if stability_percent >= 75:
        label = "High"
    elif stability_percent >= 55:
        label = "Moderate"
    else:
        label = "Low"

    return stability_percent, label


# ================= PREDICTION =================

def predict_pair(api_name, api_smiles, coformer_name, coformer_smiles):

    if not is_valid_smiles(api_smiles):
        print("❌ Invalid API SMILES")
        return None

    if not is_valid_smiles(coformer_smiles):
        print("❌ Invalid Coformer SMILES")
        return None

    api_desc = calculate_descriptors(api_smiles)
    cof_desc = calculate_descriptors(coformer_smiles)

    interaction = analyze_interaction(api_desc, cof_desc)
    synthon = analyze_synthon(api_desc, cof_desc)

    probability = calculate_probability(
        delta_pka=0.6,
        hbond=interaction,
        synthon=synthon,
        descriptor=0.7,
        solubility=0.7,
        packing=0.7,
        lattice=0.7
    )

    verdict, compatibility = classify_probability(probability)
    stability_percent, stability_label = classify_stability(probability, interaction, synthon)

    return {
        "api_name": api_name,
        "api_smiles": api_smiles,
        "coformer_name": coformer_name,
        "coformer_smiles": coformer_smiles,
        "probability": probability,
        "compatibility": compatibility,
        "stability_percent": stability_percent,
        "stability_label": stability_label,
        "verdict": verdict
    }


# ================= DISPLAY =================

def clean_name(name):
    return name.lower().replace(" ", "_")


def display_prediction(result):
    print("\n================================")
    print("AgniKristal 2.0 Prediction")
    print("================================")

    print(f"\nAPI        : {result['api_name']}")
    print(f"Coformer   : {result['coformer_name']}")

    print("\nPrediction Summary")
    print("-----------------------")
    print(f"Co-crystal Probability : {result['probability']}%")
    print(f"Compatibility          : {result['compatibility']}")
    print(f"Stability              : {result['stability_label']} ({result['stability_percent']}%)")

    print("\nFinal Verdict")
    print("-----------------------")
    print(result["verdict"])

    # ------------------------------
    # 3D STRUCTURE GENERATION
    # ------------------------------
    if COMPLEX_AVAILABLE:
        filename = f"{clean_name(result['api_name'])}_{clean_name(result['coformer_name'])}_complex.pdb"

        generate_complex(
            result["api_smiles"],
            result["coformer_smiles"],
            filename
        )

        print(f"\n3D Structure Generated : {filename}")

        # 🔥 ADD IMAGE GENERATION HERE (IMPORTANT)
        generate_cocrystal_image(
            result["api_smiles"],
            result["coformer_smiles"],
            "cocrystal.png"
        )


# ================= MAIN =================

def main():
    print("\n================================")
    print("Running AgniKristal 2.0 PRO (Direct Mode)")
    print("================================")

    api_name = input("\nEnter API name: ")
    api_smiles = input("Enter API SMILES: ")

    coformer_name = input("Enter Coformer name: ")
    coformer_smiles = input("Enter Coformer SMILES: ")

    result = predict_pair(api_name, api_smiles, coformer_name, coformer_smiles)

    if result:
        display_prediction(result)


if __name__ == "__main__":
    main()