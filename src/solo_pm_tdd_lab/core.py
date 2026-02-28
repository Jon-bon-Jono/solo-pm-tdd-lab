def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp x to [lo, hi]."""
    if lo > hi:
        raise ValueError("lo must be less than or equal to hi")
    return max(lo, min(x, hi))
