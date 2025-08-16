# Exact K <-> rho utilities (PNG-only workflows can import these)

import math
from typing import Optional

def rho_exact(K: float, r_v: float, r_f: float) -> float:
    """
    Exact constant-curvature ρ = π_v / π_f using geodesic-circle circumference laws.
      π_a(r) = π * S_K(r)/r
      S_K(r) = sin(√K r)/√K   (K>0)
               r              (K=0)
               sinh(√(-K) r)/√(-K) (K<0)
    """
    if abs(K) < 1e-14:
        return (r_f / r_v)  # S_0(r)=r
    if K > 0:
        t = math.sqrt(K)
        num = math.sin(t * r_v) / (t * r_v)
        den = math.sin(t * r_f) / (t * r_f)
        return num / den
    else:
        t = math.sqrt(-K)
        num = math.sinh(t * r_v) / (t * r_v)
        den = math.sinh(t * r_f) / (t * r_f)
        return num / den

def solve_K_hyperbolic(rho: float, r_v: float, r_f: float) -> Optional[float]:
    """
    Solve for K<0 such that rho_exact(K, r_v, r_f) == rho.
    Returns K (negative) or None if no solution in the scanned range.
    """
    if not (r_f < r_v):  # typical for K<0 to get rho>1 with these radii
        # You can still try, but most setups choose r_f < r_v
        pass

    target = rho

    def f(t):  # t = √(-K) > 0
        # rho_exact for K = -(t^2)
        num = math.sinh(t * r_v) / (t * r_v)
        den = math.sinh(t * r_f) / (t * r_f)
        return (num / den) - target

    a, b = 1e-6, 50.0
    fa, fb = f(a), f(b)
    tries = 0
    while fa * fb > 0 and tries < 8:
        b *= 1.6
        fb = f(b)
        tries += 1
    if fa * fb > 0:
        return None

    # Bisection
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < 1e-12:
            a = b = m
            break
        if fa * fm <= 0:
            b = m; fb = fm
        else:
            a = m; fa = fm
    t = 0.5 * (a + b)
    return -(t * t)

def solve_K_spherical(rho: float, r_v: float, r_f: float) -> Optional[float]:
    """
    Solve for K>0 such that rho_exact(K, r_v, r_f) == rho.
    Returns K (positive) or None if no solution bracketed.
    """
    if not (r_f > r_v):  # typical for K>0 to get rho>1 with these radii
        pass

    target = rho

    def f(t):  # t = √K
        # avoid sin near zeros in denominator
        den = math.sin(t * r_f) / (t * r_f)
        if abs(den) < 1e-14:
            return float('inf')
        num = math.sin(t * r_v) / (t * r_v)
        return (num / den) - target

    # scan for sign change (keep t small to avoid oscillations)
    lo, hi = 1e-6, 3.0
    steps = 600
    prev_t = lo; prev_f = f(prev_t)
    root_a = root_b = None
    for i in range(1, steps + 1):
        t = lo + (hi - lo) * i / steps
        val = f(t)
        if math.isfinite(prev_f) and math.isfinite(val) and prev_f * val <= 0:
            root_a, root_b = prev_t, t
            break
        prev_t, prev_f = t, val
    if root_a is None:
        return None

    # Bisection
    a, b = root_a, root_b
    fa, fb = f(a), f(b)
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = f(m)
        if not math.isfinite(fm):
            m += 1e-6; fm = f(m)
        if abs(fm) < 1e-12:
            a = b = m
            break
        if fa * fm <= 0:
            b = m; fb = fm
        else:
            a = m; fa = fm
    t = 0.5 * (a + b)
    return t * t
