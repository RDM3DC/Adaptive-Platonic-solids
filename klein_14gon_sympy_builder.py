
import sympy as sp
import json, math
import numpy as np
import pandas as pd

# === 1) Symbolic 14-gon vertices in the Poincaré disk (your formula) ===
pi = sp.pi
cosh_r = sp.cos(pi/7) / sp.sin(pi/14)
r = sp.acosh(cosh_r)
rho = sp.tanh(r)  # ≈ 0.969...
vertices_sym = [rho * sp.exp(sp.I * 2*pi * k / 14) for k in range(14)]

# Numeric (for plotting/export); center at index 14
verts_num = [(complex(v).real, complex(v).imag) for v in map(lambda z: complex(sp.N(z, 50)), vertices_sym)]
verts_num.append((0.0, 0.0))  # center

N = 14
CENTER = 14

# === 2) Boundary edges and opposite-edge pairings (reverse orientation) ===
edges = [(i, (i+1)%N) for i in range(N)]
pairing = {i: (i+7)%N for i in range(N)}  # i ↔ i+7 mod 14

# For an oriented boundary edge e=(i,i+1), its partner is e'=(j,j+1) with j=(i+7)%N,
# glued with reverse orientation: map i -> j+1 and i+1 -> j  (mod N).
glue_map = {}
for i in range(N):
    j = (i+7) % N
    glue_map[(i, (i+1)%N)] = ((j+1)%N, j)

# === 3) Triangulate the domain by a fan from the center ===
triangles = [(CENTER, i, (i+1)%N) for i in range(N)]  # 14 triangles

# === 4) Apply identifications (union-find on vertices), then deduplicate triangles/edges ===
class DSU:
    def __init__(self, n): self.p=list(range(n))
    def find(self, x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self, a,b):
        ra, rb = self.find(a), self.find(b)
        if ra!=rb: self.p[rb]=ra

dsu = DSU(N+1)
# apply boundary vertex identifications implied by each glued edge
for (a,b), (c,d) in glue_map.items():
    dsu.union(a, c)
    dsu.union(b, d)

# representative map
rep = {i: dsu.find(i) for i in range(N+1)}

# map vertices to compacted ids
uniq_reps = sorted(set(rep.values()))
id_map = {old:i for i, old in enumerate(uniq_reps)}
Vn = len(uniq_reps)

# remap triangles to canonical vertex ids
tris = []
for (u,v,w) in triangles:
    a,b,c = id_map[rep[u]], id_map[rep[v]], id_map[rep[w]]
    # sort or orient consistently to dedup
    tris.append(tuple(sorted((a,b,c))))
# dedup faces
F_set = sorted(set(tris))
Fn = len(F_set)

# build unique undirected edges from faces
E_set = set()
for a,b,c in F_set:
    e1 = tuple(sorted((a,b)))
    e2 = tuple(sorted((b,c)))
    e3 = tuple(sorted((c,a)))
    E_set.update([e1,e2,e3])
En = len(E_set)

chi = Vn - En + Fn

# === 5) Export CSV (numeric vertex coords of representatives, faces by ids) ===
# build numeric coordinates for representatives
verts_rep = []
for old in uniq_reps:
    x,y = verts_num[old]
    verts_rep.append((x,y,0.0))  # 2D disk; z=0 for convenience

# reconstruct a face list in consistent orientation using the original (unsorted) triangles
# but mapped to rep ids and then to compact ids; allow duplicates removal
faces_oriented = []
seen = set()
for (u,v,w) in triangles:
    a,b,c = id_map[rep[u]], id_map[rep[v]], id_map[rep[w]]
    key = tuple(sorted((a,b,c)))
    if key in seen: continue
    seen.add(key)
    faces_oriented.append((a,b,c))

# Save
pd.DataFrame(verts_rep, columns=["x","y","z"]).to_csv("klein_14gon_vertices.csv", index=False)
pd.DataFrame(faces_oriented, columns=["i","j","k"]).to_csv("klein_14gon_faces.csv", index=False)

# Also dump a summary JSON
summary = {
    "V": Vn, "E": En, "F": Fn, "chi": chi,
    "note": "Combinatorial triangulation of the 14-gon fan after identifications; not the {3,7} net yet."
}
with open("klein_14gon_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Summary:", summary)
