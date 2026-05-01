# core/pkamodel_engine.py

def delta_pka(api_pka, coformer_pka):
    """
    Calculate ΔpKa difference between API and coformer.
    """

    if api_pka is None or coformer_pka is None:
        raise ValueError("pKa values must not be None")

    return abs(api_pka - coformer_pka)


def delta_pka_score(api_pka, coformer_pka):
    """
    Convert ΔpKa into normalized score (0–1)
    based on pharmaceutical salt–cocrystal rule.
    """

    diff = delta_pka(api_pka, coformer_pka)

    # ΔpKa interpretation
    # <1  → strong co-crystal probability
    # 1–2 → moderate
    # 2–3 → weak
    # >3  → salt formation likely

    if diff < 1:
        score = 1.0

    elif diff < 2:
        score = 0.7

    elif diff < 3:
        score = 0.4

    else:
        score = 0.1

    return round(score, 3)