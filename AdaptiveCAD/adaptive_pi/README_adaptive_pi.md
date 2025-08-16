# Adaptive-π on AdaptiveCAD (genus-3, {3,7})

This mini-module turns a target π-ratio field ρ(x) into a per-face curvature K_f,
enforces Gauss–Bonnet for genus 3, and renders a PNG.

**Key equations**

- π_a(r) = π · S_K(r)/r,  S_K(r) = sin(√K r)/√K (K>0), r (K=0), sinh(√−K r)/√−K (K<0)
- ρ = π_v / π_f = [S_K(r_v)/r_v] / [S_K(r_f)/r_f]
- {n,q} closure: 1/n + ρ/q > 1/2; for {3,7} ⇒ ρ > 7/6
- Gauss–Bonnet (g=3): ∑_f K_f A_f = 2π(2−2g) = −8π

**Quick start**

```bash
cd AdaptiveCAD
python -m venv .venv && source .venv/bin/activate
pip install numpy matplotlib
python adaptive_pi/driver_adaptivecad.py --mode tempered --rho 1.7
# -> outputs/adaptive_pi_K_genus3.png

Wiring to your kernel

Replace the methods in KernelAdapter with your actual AdaptiveCAD API calls:
• load_genus3_mesh() → load a genus-3 surface mesh (V,F,A).
• render_face_scalar() → your renderer to a PNG.

Tweaks
• Set `--rho` to pick a constant ρ in [1.3, 2.4].
• Pass `--mode exact` to recover ρ from K via the exact sinh/sin laws (default `tempered`).
• Switch branch to "spherical" and set r_f > r_v if you want a spherical variant.
• Use your {3,7} combinatorics if you have it; this driver is geometry-first and PNG-only.

---

## What you’ll get out of the box

- A **PNG heatmap**: `outputs/adaptive_pi_K_genus3.png` showing the per-face $begin:math:text$K$end:math:text$ field consistent with your chosen $begin:math:text$\rho(\mathbf{x})$end:math:text$, **normalized to $begin:math:text$-8\pi$end:math:text$** total curvature (genus 3).

## Nice next tweaks

- Replace the proxy pretzel with your **genus-3 mesh** or a proper **Klein quartic fundamental domain** quotient mesh.
- Drop in your **{3,7} combinatorics** to visualize faces/vertices explicitly (color by vertex deficit $begin:math:text$\delta = 2\pi_f(\rho - 7/6)$end:math:text$).
- Add a **phase toggle** to render Euclidean limit ($begin:math:text$\rho=1$end:math:text$) vs adaptive ($begin:math:text$\rho>7/6$end:math:text$) side-by-side.

If you want me to tailor the `KernelAdapter` to actual function names in your `AdaptiveCAD` API, paste those names and I’ll wire the calls directly.
