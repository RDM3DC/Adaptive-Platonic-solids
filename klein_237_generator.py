"""Generate Klein {3,7} triangulation.

Constructs PSL(2,7) as 2x2 matrices over F_7, builds the (2,3,7)
permutation triple, and exports a 24-vertex, 56-face triangulation.
Vertex coordinates are placed on the unit circle (placeholder layout).
"""

import itertools
import math
import numpy as np
import pandas as pd

MOD = 7


def _normalize(mat):
    """Canonical representative modulo ±I."""
    a, b, c, d = mat
    a %= MOD; b %= MOD; c %= MOD; d %= MOD
    neg = ((-a) % MOD, (-b) % MOD, (-c) % MOD, (-d) % MOD)
    return min((a, b, c, d), neg)


def _matmul(m1, m2):
    a1, b1, c1, d1 = m1
    a2, b2, c2, d2 = m2
    return _normalize((a1 * a2 + b1 * c2,
                        a1 * b2 + b1 * d2,
                        c1 * a2 + d1 * c2,
                        c1 * b2 + d1 * d2))


def _matinv(m):
    a, b, c, d = m
    return _normalize((d, -b, -c, a))

# Enumerate PSL(2,7)
G = []
for a, b, c, d in itertools.product(range(MOD), repeat=4):
    if (a * d - b * c) % MOD == 1:
        g = _normalize((a, b, c, d))
        if g not in G:
            G.append(g)
index = {g: i for i, g in enumerate(G)}
assert len(G) == 168

# Generators of orders 2 and 3; third is derived to satisfy abc=1
A = _normalize((0, -1, 1, 0))         # order 2
B = _normalize((0, -1, 1, 1))         # order 3
C = _matinv(_matmul(A, B))           # order 7

# Permutations on the 168 darts
a = [0] * 168
b = [0] * 168
c = [0] * 168
for g in G:
    idx = index[g]
    a[idx] = index[_matmul(A, g)]
    b[idx] = index[_matmul(B, g)]
    c[idx] = index[_matmul(C, g)]

# Vertex ids from cycles of c (length 7)
vertex_of = [None] * 168
vertex_cycles = []
for i in range(168):
    if vertex_of[i] is None:
        j = i
        while vertex_of[j] is None:
            vertex_of[j] = len(vertex_cycles)
            j = c[j]
        vertex_cycles.append(None)
Vn = len(vertex_cycles)  # 24

# Triangular faces from cycles of b (length 3)
faces = []
seen = [False] * 168
for i in range(168):
    if not seen[i]:
        j = i
        tri = []
        for _ in range(3):
            seen[j] = True
            tri.append(vertex_of[j])
            j = b[j]
        faces.append(tuple(tri))
Fn = len(faces)  # 56

# Place vertices on a unit circle
angles = np.linspace(0, 2 * math.pi, Vn, endpoint=False)
verts = np.stack([np.cos(angles), np.sin(angles), np.zeros_like(angles)], axis=1)

# Export CSVs
pd.DataFrame(verts, columns=["x", "y", "z"]).to_csv("klein_vertices.csv", index=False)
pd.DataFrame(faces, columns=["i", "j", "k"]).to_csv("klein_faces.csv", index=False)

# Summary
En = len({tuple(sorted(e)) for tri in faces for e in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0]))})
chi = Vn - En + Fn
print({"V": Vn, "E": En, "F": Fn, "chi": chi})
