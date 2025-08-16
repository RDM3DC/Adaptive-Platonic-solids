# Adaptive-π Platonic Catalogue

**One-liner:** A tiny research repo showing how an adaptive π framework expands the classical Platonic catalogue.  
We encode the existence rule with the π-ratio ρ := π_v / π_f and test which regular `{n,q}` pairs satisfy
`1/n + (ρ/q) > 1/2`.

---

## Key idea

- Interior angle (regular n-gon): `θ_n(π_a) = (1 - 2/n) · π_a`
- Vertex closure (q meet at each vertex): `q · θ_n(π_f) < 2 · π_v`
- Define `ρ := π_v / π_f`  →  **Master inequality:**  
  **`1/n + (ρ / q) > 1/2`**

Angle deficit (per vertex):  
`δ = 2π_f [ ρ − ρ*(n,q) ]`, where `ρ*(n,q) = q (1/2 − 1/n) = q(n−2)/(2n)`.

### Euclidean recovery
If `ρ = 1` we get the classical condition `1/n + 1/q > 1/2` → exactly five Platonic solids.

### Example
`{3,7}` needs `ρ > 7/6 ≈ 1.1667`.  
At `ρ = 1.20` the normalized surplus is `δ/(2π_f) = 1.20 − 1.1667 ≈ 0.0333` (3.33%).

---

## What’s in this repo

- `src/closure.py` — Core math utilities (ρ*, feasibility tests, counts).
- `src/generate_tables.py` — Prints admissible `{n,q}` for a chosen ρ (and basic topology notes).
- `src/render_ngon_star.py` — Saves a **PNG** of a simple `{n,q}` “star” patch (no OBJ).
- `src/phase_diagram.py` — Saves a **PNG** heatmap showing which `{n,q}` are enabled at a given ρ.
- `src/equations_card.py` — Saves a **PNG** card with the core equations (for posts/figures).

Outputs are written to `outputs/`.

For a CAD-focused implementation, see [AdaptiveCAD](https://github.com/RDM3DC/AdaptiveCAD).

---

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Quick start
    1.List admissible {n,q} at ρ=1.20:

python src/generate_tables.py --rho 1.20 --nmax 20 --qmax 20

    2.Render a {3,7} PNG (no OBJ):

python src/render_ngon_star.py --n 3 --q 7 --outfile outputs/ngon_3_7.png

    3.Phase diagram at ρ=1.20:

python src/phase_diagram.py --rho 1.20 --nmax 20 --qmax 20 --outfile outputs/phase_rho_1_20.png

    4.Equation card PNG:

python src/equations_card.py --outfile outputs/adaptive_pi_equations.png
```

---

Notes on topology

Combinatorics is π-independent. With nF=2E, qV=2E, and V−E+F=χ, a sphere (χ=2) requires
1/n + 1/q > 1/2. Pairs with 1/n + 1/q ≤ 1/2 live as regular maps on tori or higher-genus surfaces.

---

Citation

If you use this idea, please cite:

McKenna, R. (RDM3DC). Adaptive-π vertex closure and the expanded Platonic catalogue (2025). GitHub: rdm3dc/adaptive-pi-platonic

(You can also edit CITATION.cff with your author details.)
