# src/generate_tables.py
import argparse
from closure import feasible, rho_star, delta_normalized


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, required=True, help="π-ratio ρ = π_v/π_f")
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--qmax", type=int, default=20)
    args = ap.parse_args()

    rho = args.rho
    print(f"# Admissible {{n,q}} for ρ = {rho:.4f}  (condition: 1/n + ρ/q > 1/2)\n")
    print(f"{'n':>3} {'q':>3} {'ρ*':>8} {'δ/(2π_f)':>10}")
    print("-"*30)
    for n in range(3, args.nmax+1):
        for q in range(3, args.qmax+1):
            if feasible(n, q, rho):
                rs = rho_star(n, q)
                dn = delta_normalized(n, q, rho)
                print(f"{n:3d} {q:3d} {rs:8.4f} {dn:10.4f}")


if __name__ == "__main__":
    main()
