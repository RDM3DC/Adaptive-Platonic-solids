
# Reads the CSV produced by the builder and recomputes V/E/F/χ. Also reports Gauss–Bonnet target.
import pandas as pd, math, json

V = pd.read_csv("klein_14gon_vertices.csv").to_numpy()
F = pd.read_csv("klein_14gon_faces.csv").to_numpy(dtype=int)

Vn = V.shape[0]
# unique undirected edges from faces
E_set = set()
for a,b,c in F:
    E_set.add(tuple(sorted((a,b))))
    E_set.add(tuple(sorted((b,c))))
    E_set.add(tuple(sorted((c,a))))
En = len(E_set)
Fn = F.shape[0]
chi = Vn - En + Fn

summary = {"V": int(Vn), "E": int(En), "F": int(Fn), "chi": int(chi),
           "GB_total_curvature": 2*math.pi*chi, "expected_for_g3": -8*math.pi}

with open("klein_14gon_verify.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Verify:", summary)
