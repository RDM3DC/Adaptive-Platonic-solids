"""Gauss--Bonnet check for arbitrary per-face K and area."""
import sys, math
import pandas as pd

if len(sys.argv) != 3:
    raise SystemExit("usage: python gb_check_adaptive_min.py face_areas.csv K_face.csv")
A = pd.read_csv(sys.argv[1]).to_numpy().ravel()
K = pd.read_csv(sys.argv[2]).to_numpy().ravel()
curv = float((A * K).sum())
print({"integral_KdA": curv, "target": -8 * math.pi})
