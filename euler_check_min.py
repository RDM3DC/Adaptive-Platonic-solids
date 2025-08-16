"""Minimal Euler characteristic check for a triangulated mesh."""
import sys
import pandas as pd

if len(sys.argv) != 3:
    raise SystemExit("usage: python euler_check_min.py vertices.csv faces.csv")

V = pd.read_csv(sys.argv[1]).to_numpy()
F = pd.read_csv(sys.argv[2]).to_numpy(dtype=int)
Vn = V.shape[0]
E = set()
for a, b, c in F:
    E.add(tuple(sorted((a, b))))
    E.add(tuple(sorted((b, c))))
    E.add(tuple(sorted((c, a))))
En = len(E)
Fn = F.shape[0]
chi = Vn - En + Fn
print({"V": Vn, "E": En, "F": Fn, "chi": chi})
