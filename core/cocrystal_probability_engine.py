# core/cocrystal_probability_engine.py

def calculate_probability(
    delta_pka,
    hbond,
    synthon,
    descriptor,
    solubility,
    packing,
    lattice
):
    """
    Calculate overall co-crystal formation probability (0–100%)
    based on weighted chemical features.
    """

    factors = {
        "delta_pka": delta_pka,
        "hbond": hbond,
        "synthon": synthon,
        "descriptor": descriptor,
        "solubility": solubility,
        "packing": packing,
        "lattice": lattice
    }

    # Validate scores
    for name, value in factors.items():
        if not 0 <= value <= 1:
            raise ValueError(f"{name} score must be between 0 and 1")

    score = (
        delta_pka * 0.25 +
        hbond * 0.20 +
        synthon * 0.15 +
        descriptor * 0.10 +
        solubility * 0.10 +
        packing * 0.10 +
        lattice * 0.10
    )

    return round(score * 100, 2)