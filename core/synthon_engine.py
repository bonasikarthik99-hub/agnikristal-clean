# core/synthon_engine.py

def analyze_synthon(api_desc, coformer_desc):
    """
    Supramolecular synthon compatibility scoring
    Used for AgniKristal co-crystal prediction
    """

    api_hbd = api_desc.get("HBD", 0)
    api_hba = api_desc.get("HBA", 0)

    cof_hbd = coformer_desc.get("HBD", 0)
    cof_hba = coformer_desc.get("HBA", 0)

    # possible heterosynthon interactions
    donor_acceptor = min(api_hbd, cof_hba)

    # reverse heterosynthon
    acceptor_donor = min(api_hba, cof_hbd)

    total_synthon = donor_acceptor + acceptor_donor

    max_possible = max(api_hbd + api_hba, cof_hbd + cof_hba)

    if max_possible == 0:
        return 0

    synthon_score = total_synthon / max_possible

    return round(synthon_score, 3)