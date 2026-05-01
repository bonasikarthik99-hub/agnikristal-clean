from rdkit import Chem

def batch_screen(api_smiles, coformers):

    results = []

    api_mol = Chem.MolFromSmiles(api_smiles)

    for name, smiles in coformers:

        cof_mol = Chem.MolFromSmiles(smiles)

        score = 0

        if api_mol and cof_mol:
            score = api_mol.GetNumAtoms() + cof_mol.GetNumAtoms()

        prediction = "Possible cocrystal" if score > 20 else "Low probability"

        results.append({
            "Coformer": name,
            "Final Score": score,
            "Prediction": prediction
        })

    return results