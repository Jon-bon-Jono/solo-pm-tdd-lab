def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp x to [lo, hi]."""
    if lo > hi: raise ValueError("In clamp lo must be < hi.")
    return max(lo, min(x, hi))