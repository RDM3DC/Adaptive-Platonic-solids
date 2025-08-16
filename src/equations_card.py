# src/equations_card.py
import argparse
import matplotlib.pyplot as plt

CARD = r"""
Adaptive-π Vertex Closure (Cheat Sheet)

1) π_a small-circle (Gaussian curvature K at scale r):
   π_a(r) ≈ π · (1 − K r² / 6)

2) Interior angle (regular n-gon):
   θ_n(π_a) = (1 − 2/n) · π_a

3) Closure (q meet at a vertex):
   q · θ_n(π_f) < 2 · π_v

4) π-ratio:
   ρ := π_v / π_f

5) Master inequality:
   1/n + (ρ / q) > 1/2

6) Threshold:
   ρ*(n,q) = q (1/2 − 1/n) = q (n−2) / (2n)

7) Angle deficit:
   δ = 2π_f [ ρ − ρ*(n,q) ]

8) Euler (topology):
   nF = 2E, qV = 2E,  V − E + F = χ
   E = χ / ( 2 (1/n + 1/q − 1/2) )
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outfile", type=str, default="outputs/adaptive_pi_equations.png")
    args = ap.parse_args()

    fig, ax = plt.subplots(figsize=(8,6))
    ax.axis('off')
    ax.text(0.0, 1.0, CARD, va="top", fontsize=12, family="monospace")
    fig.tight_layout()
    fig.savefig(args.outfile, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
