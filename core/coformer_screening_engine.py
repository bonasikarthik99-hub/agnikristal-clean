import pandas as pd
import os
from core.descriptor_engine import calculate_descriptors
from core.interaction_engine import analyze_interaction
from core.synthon_engine import analyze_synthon


def load_coformers():
    """
    Load coformer database from data folder.
    """

    base_dir = os.path.dirname(os.path.dirname(__file__))

    file_path = os.path.join(base_dir, "data", "coformer_database.csv")

    return pd.read_csv(file_path)


def suggest_coformers(api_smiles, top_n=10):

    api_desc = calculate_descriptors(api_smiles)

    df = load_coformers()

    results = []

    for _, row in df.iterrows():

        name = row["Coformer"]
        smiles = row["Coformer_SMILES"]

        try:

            cof_desc = calculate_descriptors(smiles)

            interaction = analyze_interaction(api_desc, cof_desc)
            synthon = analyze_synthon(api_desc, cof_desc)

            score = (interaction * 0.6) + (synthon * 0.4)

            results.append((name, round(score * 100, 2)))

        except:
            continue

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results[:top_n]