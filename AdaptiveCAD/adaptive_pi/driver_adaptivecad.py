"""
AdaptiveCAD driver (PNG-only):
- Assign a {3,7} combinatorics on a genus-3 surface
- Choose a rho(x) field (constant 1.20 by default)
- Solve per-face K from rho using exact formulas
- Enforce Gauss–Bonnet sum_f K_f A_f = -8π (g=3)
- Render per-face K as a heatmap

Wire the 'KernelAdapter' methods to your AdaptiveCAD kernel.
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict, Tuple

from .solve_curvature import solve_K_hyperbolic, solve_K_spherical, rho_exact

# ------- 0) Replace this shim with your real AdaptiveCAD API calls -------
class KernelAdapter:
    def __init__(self):
        # TODO: connect to AdaptiveCAD kernel if needed
        pass

    def load_genus3_mesh(self):
        """
        Return a simple struct with:
            .V  (N_v x 3) vertices (np.ndarray)
            .F  (N_f x 3) faces    (np.ndarray int)
            .A  (N_f,)   face areas (np.ndarray float)
        You can swap this with your kernel's actual mesh.
        """
        # Placeholder: a coarse triangulated "pretzel" proxy.
        # Replace with: self.kernel.load_template('genus3') or similar.
        theta = np.linspace(0, 2*np.pi, 64, endpoint=False)
        loops = []
        for cx in [-2.0, 0.0, 2.0]:
            x = np.cos(theta) + cx
            y = np.sin(theta)
            z = 0.15 * np.sin(3 * theta)
            loops.append(np.stack([x, y, z], axis=1))
        V = np.vstack(loops)
        # Make a trivial fan-triangulation per loop (proxy)
        F = []
        base = 0
        n = len(theta)
        for k in range(3):
            for i in range(n):
                F.append([base + i, base + ((i + 1) % n), base + (i + n//2) % n])
            base += n
        F = np.array(F, dtype=int)

        # Compute per-face areas
        def tri_area(a,b,c):
            return 0.5 * np.linalg.norm(np.cross(b - a, c - a))
        A = np.array([tri_area(V[i], V[j], V[k]) for i,j,k in F], dtype=float)

        class Mesh: pass
        m = Mesh()
        m.V, m.F, m.A = V, F, A
        return m

    def render_face_scalar(self, mesh, values: np.ndarray, title: str, outfile: str):
        """
        Render a flat PNG of per-face scalar (heatmap-ish). Replace with your renderer.
        """
        # Quick barycenter scatter with triangulation outline
        V, F = mesh.V, mesh.F
        bary = V[F].mean(axis=1)
        fig, ax = plt.subplots(figsize=(7,5))
        t = ax.tripcolor(V[:,0], V[:,1], F, facecolors=values, shading='flat')
        ax.triplot(V[:,0], V[:,1], F, linewidth=0.2)
        ax.set_aspect('equal'); ax.axis('off')
        cbar = plt.colorbar(t, ax=ax)
        cbar.set_label("K (curvature)")
        ax.set_title(title)
        fig.tight_layout()
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        fig.savefig(outfile, dpi=220, bbox_inches="tight")
        plt.close(fig)

# ------- 1) Choose your rho(x) and (r_v, r_f) maps -------
def constant_field(value: float) -> Callable[[np.ndarray], float]:
    """Return a function rho(x) = value for any x."""
    return lambda x: value

def concentric_bumps(center=(0.0,0.0,0.0), inner=1.15, outer=1.25) -> Callable[[np.ndarray], float]:
    """Example spatially varying rho(x)."""
    cx, cy, cz = center
    def fn(x):
        r = np.linalg.norm(x - np.array([cx, cy, cz]))
        return inner + (outer - inner) * (1.0 / (1.0 + np.exp(10*(r-1.2))))
    return fn

def constant_scales(r_v=1.0, r_f=0.8) -> Callable[[np.ndarray], Tuple[float,float]]:
    return lambda x: (r_v, r_f)

# ------- 2) Solve per-face K from rho (choose branch) -------
def solve_per_face_K(mesh, rho_fn, scales_fn, branch="hyperbolic"):
    """
    For each face, evaluate rho at barycenter, pick (r_v, r_f), solve K from rho.
    branch: 'hyperbolic' (K<0) or 'spherical' (K>0)
    """
    V, F = mesh.V, mesh.F
    bary = V[F].mean(axis=1)
    K = np.zeros(len(F), dtype=float)

    for idx, p in enumerate(bary):
        rho = rho_fn(p)
        r_v, r_f = scales_fn(p)
        if branch == "hyperbolic":
            k = solve_K_hyperbolic(rho=rho, r_v=r_v, r_f=r_f)
        else:
            k = solve_K_spherical(rho=rho, r_v=r_v, r_f=r_f)
        if k is None or (branch == "hyperbolic" and k >= 0) or (branch == "spherical" and k <= 0):
            # fallback to small-r linearization (first order)
            # K ≈ 6(ρ-1)/(r_f^2 - r_v^2)
            denom = (r_f*r_f - r_v*r_v)
            if abs(denom) < 1e-12:
                k = -1.0 if branch == "hyperbolic" else +1.0
            else:
                k = 6.0 * (rho - 1.0) / denom
                if branch == "hyperbolic": k = min(k, -1e-6)
                else: k = max(k, 1e-6)
        K[idx] = k
    return K

# ------- 3) Enforce Gauss–Bonnet for genus 3 -------
def gauss_bonnet_normalize(mesh, K_face: np.ndarray, target_chi: int = -4) -> np.ndarray:
    """
    Scale K_face so that sum_f K_f A_f = 2π χ.
    For genus g=3, χ = 2 - 2g = -4 → target integral = -8π.
    """
    A = mesh.A
    current = float((K_face * A).sum())
    target = 2.0 * math.pi * float(target_chi)
    if abs(current) < 1e-14:
        return K_face
    s = target / current
    return K_face * s


def rho_from_K(point, K_of_point, mode="tempered", r_v=1.0, r_f=0.8, c=None):
    """
    Compute ρ at a point given K(point).

    mode:
      - "tempered": ρ ≈ 1 + c·K  (requires c; if None, uses (r_f^2 - r_v^2)/6)
      - "exact":    ρ = [S_K(r_v)/r_v] / [S_K(r_f)/r_f]  with sin/sinh laws
    """
    K = K_of_point(point)
    if mode == "tempered":
        if c is None:
            c = (r_f*r_f - r_v*r_v)/6.0
        return 1.0 + c * K
    else:  # exact
        if abs(K) < 1e-12:
            return 1.0
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

# ------- 4) CLI-style main -------
def main():
    ka = KernelAdapter()
    mesh = ka.load_genus3_mesh()

    # Pick your field: constant ρ(x)=1.20 is a good start for {3,7}.
    rho_fn = constant_field(1.20)
    # Scales: typical choice for hyperbolic branch: r_v=1.0, r_f=0.8
    scales_fn = constant_scales(r_v=1.0, r_f=0.8)

    # Solve K per face (hyperbolic branch for {3,7})
    K_face = solve_per_face_K(mesh, rho_fn, scales_fn, branch="hyperbolic")

    # Enforce Gauss–Bonnet for g=3 → χ=-4
    K_face = gauss_bonnet_normalize(mesh, K_face, target_chi=-4)

    # Render PNG heatmap of curvature
    ka.render_face_scalar(mesh, K_face, title="Adaptive-π: per-face K (g=3, {3,7})",
                          outfile="outputs/adaptive_pi_K_genus3.png")

    # Example: recover ρ from K using a tempered linearization
    MODE = "tempered"   # or "exact"
    R_V, R_F = 2.09, 0.8
    C_CONST = -0.623
    bary = mesh.V[mesh.F].mean(axis=1)
    rho_faces = np.array([
        rho_from_K(p, lambda _p, k=K_face[idx]: k, mode=MODE, r_v=R_V, r_f=R_F, c=C_CONST)
        for idx, p in enumerate(bary)
    ])
    ka.render_face_scalar(mesh, rho_faces, title="Adaptive-π: ρ from K",
                          outfile="outputs/adaptive_pi_rho_genus3.png")

if __name__ == "__main__":
    main()
