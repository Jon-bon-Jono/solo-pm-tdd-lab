def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp x to [lo, hi]."""
    if lo > hi: raise ValueError("clamp: lo > hi.")
    return max(lo, min(x, hi))