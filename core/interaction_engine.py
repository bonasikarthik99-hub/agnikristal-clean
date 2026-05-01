# core/interaction_engine.py

def analyze_interaction(api_desc, coformer_desc):
    """
    Hydrogen bond interaction scoring between API and coformer.
    Compatible with AgniKristal 1.x logic but slightly improved.
    """

    api_hbd = api_desc.get("HBD", 0)
    api_hba = api_desc.get("HBA", 0)

    cof_hbd = coformer_desc.get("HBD", 0)
    cof_hba = coformer_desc.get("HBA", 0)

    score = 0

    # API donor → coformer acceptor
    donor_acceptor = min(api_hbd, cof_hba)

    # API acceptor → coformer donor
    acceptor_donor = min(api_hba, cof_hbd)

    score = donor_acceptor + acceptor_donor

    # normalize score (0–1)
    max_possible = max(api_hbd + api_hba, cof_hbd + cof_hba)

    if max_possible == 0:
        return 0

    normalized_score = score / max_possible

    return round(normalized_score, 3)