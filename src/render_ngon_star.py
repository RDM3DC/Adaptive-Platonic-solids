# src/render_ngon_star.py
import argparse
import numpy as np
import matplotlib.pyplot as plt


def render_ngon_star(n: int, q: int, R: float = 1.0, outfile: str = "outputs/ngon_star.png"):
    """
    Draws a simple 2D patch: q regular n-gons meeting at a central vertex.
    This is a schematic visualization, not a geometric proof.
    """
    fig, ax = plt.subplots(figsize=(6,6))
    # Each "n-gon" here is represented by an isosceles wedge approximating one face at the central vertex.
    for k in range(q):
        a0 = 2*np.pi * k / q
        a1 = 2*np.pi * (k+1) / q
        # triangles/wedges around the center
        ax.fill([0, R*np.cos(a0), R*np.cos(a1)],
                [0, R*np.sin(a0), R*np.sin(a1)],
                facecolor='lightsteelblue', edgecolor='k', linewidth=0.8)

    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Schematic patch for {{{n},{q}}}", fontsize=14)
    fig.tight_layout()
    fig.savefig(outfile, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--outfile", type=str, default="outputs/ngon_star.png")
    args = ap.parse_args()
    render_ngon_star(args.n, args.q, outfile=args.outfile)


if __name__ == "__main__":
    main()
