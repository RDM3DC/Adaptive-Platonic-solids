# Render \u03c1 on a genus-3 mesh via your AdaptiveCAD kernel as a PNG.
# Supports mode="tempered" (\u03c1 \u2248 1 + cK) and mode="exact" (sinh/sin laws).

import math
import json
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ==== USER PARAMS (adjust as you like) ====
MODE   = "tempered"           # "tempered" or "exact"
R_V    = 2.09                 # for exact mode or to derive c
R_F    = 0.80
C_CONST= -0.623               # used when MODE=="tempered"
R_MODEL= 1.30                 # radius used in K(r) mapping
K0     = -26.8                # K(r) = K0 + β r^2
BETA   = 12.5
OUTPNG = "outputs/adaptivecad_rho.png"
# ==========================================

# ---- exact \u03c1(K; r_v, r_f) ----
def rho_exact(K, rv, rf):
    if abs(K) < 1e-14:
        return 1.0
    if K > 0:
        t = math.sqrt(K)
        num = math.sin(t * rv) / (t * rv)
        den = math.sin(t * rf) / (t * rf)
    else:
        t = math.sqrt(-K)
        num = math.sinh(t * rv) / (t * rv)
        den = math.sinh(t * rf) / (t * rf)
    return num / den

def rho_value(K, mode="tempered", rv=R_V, rf=R_F, c=C_CONST):
    if mode == "tempered":
        if c is None:
            c = (rf * rf - rv * rv) / 6.0
        return 1.0 + c * K
    else:
        return rho_exact(K, rv, rf)

def load_mesh_from_adaptivecad():
    """
    Load mesh data from CSV files shipped with the repository.
    Returns:
        V: (N_v,3) float vertices
        F: (N_f,3) int faces
        A: (N_f,)   float face areas
    Replace this with calls to your AdaptiveCAD kernel as needed.
    """
    root = Path(__file__).resolve().parent.parent.parent
    V = np.loadtxt(root / "user_params_vertices.csv", delimiter=",", skiprows=1)
    F = np.loadtxt(root / "user_params_faces.csv", delimiter=",", skiprows=1, dtype=int)
    A = np.loadtxt(root / "user_params_face_areas.csv", delimiter=",", skiprows=1)
    return V, F, A

def render_face_scalar_png(V, F, values, outfile, title=""):
    """Render per-face scalar values to a PNG using matplotlib."""
    fig, ax = plt.subplots(figsize=(7, 5))
    t = ax.tripcolor(V[:, 0], V[:, 1], F, facecolors=values, shading="flat")
    ax.triplot(V[:, 0], V[:, 1], F, linewidth=0.2, color="k")
    ax.set_aspect("equal")
    ax.axis("off")
    cbar = plt.colorbar(t, ax=ax)
    cbar.set_label("\u03c1")
    ax.set_title(title)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    fig.savefig(outfile, dpi=220, bbox_inches="tight")
    plt.close(fig)

def main():
    # === 1) Load mesh from AdaptiveCAD ===
    V, F, A = load_mesh_from_adaptivecad()
    V = np.asarray(V, float)
    F = np.asarray(F, int)
    A = np.asarray(A, float)
    bary = V[F].mean(axis=1)

    # === 2) Map radii to [0, R_MODEL] and build raw K(r) ===
    r_mesh = np.linalg.norm(bary, axis=1)
    r_scale = R_MODEL / r_mesh.max()
    r_model = r_scale * r_mesh
    K_raw = K0 + BETA * (r_model ** 2)

    # === 3) Enforce Gauss–Bonnet: sum_f K_f A_f = -8π (g=3) ===
    target = -8.0 * math.pi
    current = float((K_raw * A).sum())
    s = target / current
    K_face = s * K_raw

    # === 4) Build \u03c1 per face ===
    rho_face = np.array([
        rho_value(k, MODE, R_V, R_F, C_CONST) for k in K_face
    ], float)

    # === 5) Render PNG with AdaptiveCAD’s renderer ===
    render_face_scalar_png(V, F, rho_face, OUTPNG, title=f"\u03c1 ({MODE})")

    # === 6) Save a tiny JSON with stats so we can sanity-check ===
    stats = {
        "mode": MODE,
        "r_v": R_V,
        "r_f": R_F,
        "c": C_CONST,
        "r_scale": r_scale,
        "GB_scale": s,
        "GB_sum_KA": float((K_face * A).sum()),
        "GB_target": target,
        "K_min": float(K_face.min()),
        "K_max": float(K_face.max()),
        "K_mean": float(K_face.mean()),
        "rho_min": float(rho_face.min()),
        "rho_max": float(rho_face.max()),
        "rho_mean": float(rho_face.mean()),
    }
    with open(OUTPNG.replace(".png", "_stats.json"), "w") as f:
        json.dump(stats, f, indent=2)
    print("Wrote:", OUTPNG)

if __name__ == "__main__":
    main()
