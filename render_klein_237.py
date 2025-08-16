"""Render per-face curvature for the Klein {3,7} mesh."""
import numpy as np
import pandas as pd
from AdaptiveCAD.adaptive_pi.driver_adaptivecad import (
    KernelAdapter,
    constant_field,
    constant_scales,
    solve_per_face_K,
    gauss_bonnet_normalize,
)

V = pd.read_csv("klein_vertices.csv").to_numpy(float)
F = pd.read_csv("klein_faces.csv").to_numpy(int)

# face areas
def tri_area(a, b, c):
    return 0.5 * np.linalg.norm(np.cross(b - a, c - a))
A = np.array([tri_area(V[i], V[j], V[k]) for i, j, k in F], dtype=float)

class Mesh:
    pass
mesh = Mesh()
mesh.V, mesh.F, mesh.A = V, F, A

rho_fn = constant_field(1.7)
scales_fn = constant_scales()
K_face = solve_per_face_K(mesh, rho_fn, scales_fn, branch="hyperbolic")
K_face = gauss_bonnet_normalize(mesh, K_face, target_chi=-4)

# save for GB check
pd.DataFrame(A, columns=["A"]).to_csv("face_areas.csv", index=False)
pd.DataFrame(K_face, columns=["K"]).to_csv("K_face.csv", index=False)

KernelAdapter().render_face_scalar(
    mesh, K_face, "Klein {3,7} K", "outputs/klein_curvature.png"
)
