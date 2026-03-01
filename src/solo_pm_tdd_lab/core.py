import math
from typing import Iterable, List, Union

Number = Union[int, float]

def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp x to [lo, hi]."""
    #HI
    if lo > hi:
        raise ValueError("lo must be less than or equal to hi")
    return max(lo, min(x, hi))

def zscore(
    data: Iterable[Number],
    *,
    ddof: int = 0,
    nan_policy: str = "omit",
) -> List[float]:
    """
    Compute z-scores for 1D data with NaN handling.

    Parameters
    ----------
    data:
        1D iterable of numbers (ints/floats). Output is always floats.
    ddof:
        Delta degrees of freedom for variance: var = M2 / (n - ddof).
        If (n - ddof) <= 0, z-scores are undefined -> returns NaNs (except NaN inputs stay NaN).
    nan_policy:
        - "omit": ignore NaNs when computing mean/std; keep NaNs in output positions.
        - "propagate": if any NaN exists, return all NaNs.
        - "raise": if any NaN exists, raise ValueError.

    Behavior notes
    --------------
    - If effective std == 0 and defined, returns 0.0 for all non-NaN entries (constant input -> zero z-scores).
    - If there are no non-NaN values (all NaNs), returns all NaNs.
    """
    if ddof < 0:
        raise ValueError("ddof must be >= 0")

    if nan_policy not in {"omit", "propagate", "raise"}:
        raise ValueError(f"Invalid nan_policy: {nan_policy!r}")

    xs = [float(x) for x in data]
    if not xs:
        return []

    any_nan = any(math.isnan(x) for x in xs)
    if any_nan:
        if nan_policy == "raise":
            raise ValueError("NaN encountered with nan_policy='raise'")
        if nan_policy == "propagate":
            return [math.nan] * len(xs)
        # nan_policy == "omit" -> keep going

    # Welford's online algorithm over non-NaNs (or all values if no NaNs present)
    mean = 0.0
    m2 = 0.0
    n = 0

    for x in xs:
        if math.isnan(x):
            continue
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        m2 += delta * delta2

    # If all values were NaN
    if n == 0:
        return [math.nan] * len(xs)

    denom = n - ddof
    if denom <= 0:
        # Undefined variance/std -> z-scores undefined for non-NaNs
        return [math.nan if not math.isnan(x) else math.nan for x in xs]

    var = m2 / denom
    # Guard tiny negative due to floating round-off
    if var < 0.0 and abs(var) < 1e-15:
        var = 0.0

    if var < 0.0:
        # Something very wrong numerically; treat as undefined
        return [math.nan if not math.isnan(x) else math.nan for x in xs]

    std = math.sqrt(var)

    # Constant slice (std == 0): define z-score as 0.0 for non-NaNs
    if std == 0.0:
        return [math.nan if math.isnan(x) else 0.0 for x in xs]

    return [math.nan if math.isnan(x) else (x - mean) / std for x in xs]

