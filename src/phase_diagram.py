# src/phase_diagram.py
import argparse
import numpy as np
import matplotlib.pyplot as plt
from closure import feasible


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, required=True)
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--qmax", type=int, default=20)
    ap.add_argument("--outfile", type=str, default="outputs/phase.png")
    args = ap.parse_args()

    nmax, qmax = args.nmax, args.qmax
    Z = np.zeros((nmax-2, qmax-2), dtype=int)  # index 0 -> n=3

    for i, n in enumerate(range(3, nmax+1)):
        for j, q in enumerate(range(3, qmax+1)):
            Z[i, j] = 1 if feasible(n, q, args.rho) else 0

    fig, ax = plt.subplots(figsize=(7,6))
    im = ax.imshow(Z, origin='lower', aspect='auto', interpolation='nearest')
    ax.set_xlabel("q (faces at vertex)")
    ax.set_ylabel("n (gon sides)")
    ax.set_xticks(np.arange(0, qmax-2, 2), labels=[str(q) for q in range(3, qmax+1, 2)])
    ax.set_yticks(np.arange(0, nmax-2, 2), labels=[str(n) for n in range(3, nmax+1, 2)])
    ax.set_title(f"Existence map at ρ = {args.rho}")
    fig.colorbar(im, ax=ax, label="feasible (1=yes, 0=no)")
    fig.tight_layout()
    fig.savefig(args.outfile, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
