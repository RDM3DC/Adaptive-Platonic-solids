# src/closure.py
import math
from typing import List, Tuple


def rho_star(n: int, q: int) -> float:
    """Threshold ρ* = q (1/2 - 1/n) = q (n-2)/(2n)."""
    return q * (0.5 - 1.0/n)


def feasible(n: int, q: int, rho: float) -> bool:
    """Master inequality: 1/n + (rho/q) > 1/2."""
    return (1.0/n) + (rho / q) > 0.5


def delta_normalized(n: int, q: int, rho: float) -> float:
    """δ / (2π_f) = ρ − ρ*."""
    return rho - rho_star(n, q)


def euler_counts(n: int, q: int, chi: int) -> Tuple[int, int, int]:
    """
    E = chi / [ 2 (1/n + 1/q - 1/2) ]
    F = 2E / n,  V = 2E / q
    Returns (V, E, F). Values are integers if chi is compatible with (n,q).
    """
    denom = 2.0 * ((1.0/n) + (1.0/q) - 0.5)
    E = chi / denom
    V = 2.0 * E / q
    F = 2.0 * E / n
    return int(round(V)), int(round(E)), int(round(F))


def genus_from_chi(chi: int) -> int:
    """For orientable closed surfaces: chi = 2 - 2g  -> g = (2 - chi)/2."""
    return (2 - chi) // 2
