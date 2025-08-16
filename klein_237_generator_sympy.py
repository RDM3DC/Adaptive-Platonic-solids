
# klein_237_generator_sympy.py
# SymPy PermutationGroup build of the Klein quartic {3,7} triangulation using PSL(2,7).
import itertools, csv, math
import sympy as sp
from sympy.combinatorics import Permutation

MOD = 7

def det(A):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % MOD

def canon(A):
    B = ((-A[0][0])%MOD, (-A[0][1])%MOD), ((-A[1][0])%MOD, (-A[1][1])%MOD)
    tA = (A[0][0],A[0][1],A[1][0],A[1][1])
    tB = (B[0][0],B[0][1],B[1][0],B[1][1])
    return A if tA <= tB else B

def mat_mul(A,B):
    a,b,c,d = A[0][0],A[0][1],A[1][0],A[1][1]
    e,f,g,h = B[0][0],B[0][1],B[1][0],B[1][1]
    return (
        ((a*e + b*g) % MOD, (a*f + b*h) % MOD),
        ((c*e + d*g) % MOD, (c*f + d*h) % MOD)
    )

# Enumerate PSL(2,7) reps
SL = []
for a,b,c,d in itertools.product(range(MOD), repeat=4):
    A = ((a,b),(c,d))
    if det(A) == 1 % MOD:
        SL.append(A)

PSL = []
seen = set()
for A in SL:
    C = canon(A)
    t = (C[0][0],C[0][1],C[1][0],C[1][1])
    if t not in seen:
        seen.add(t)
        PSL.append(C)
assert len(PSL)==168

index = { (A[0][0],A[0][1],A[1][0],A[1][1]) : i for i,A in enumerate(PSL) }
def idx(A):
    t = (A[0][0],A[0][1],A[1][0],A[1][1])
    return index[t]

def prod_idx(i,j):
    A,B = PSL[i], PSL[j]
    C = canon(mat_mul(A,B))
    return idx(C)

I = ((1,0),(0,1))
I_idx = idx(canon(I))

def order_of(g_idx, limit=1000):
    i = g_idx
    for k in range(1, limit+1):
        if i == I_idx:
            return k
        i = prod_idx(i, g_idx)
    return None

# find S (order 2), R (order 3) with SR order 7
by_order = {}
for i in range(168):
    o = order_of(i, limit=1000)
    by_order.setdefault(o, []).append(i)

S_idx=R_idx=None
for s in by_order.get(2, []):
    for r in by_order.get(3, []):
        sr = prod_idx(s,r)
        if order_of(sr, limit=1000)==7:
            S_idx, R_idx = s, r
            break
    if S_idx is not None: break

def right_mul_perm(g_idx):
    return [prod_idx(i,g_idx) for i in range(168)]

r = right_mul_perm(R_idx)  # faces (3-cycles)
s = right_mul_perm(S_idx)  # edges (2-cycles)

# vertex permutation = s∘r
v = [ s[r[i]] for i in range(168) ]

# Wrap into SymPy Permutations (one-line form)
perm_r = Permutation(r)
perm_s = Permutation(s)
perm_v = Permutation(v)

# Get cycles
faces_darts = [c for c in perm_r.cyclic_form if len(c)==3]
edges_darts = [c for c in perm_s.cyclic_form if len(c)==2]
verts_darts = [c for c in perm_v.cyclic_form if len(c)==7]

assert len(faces_darts)==56
assert len(edges_darts)==84
assert len(verts_darts)==24

# Map each dart to a vertex id by its 7-cycle index
dart_to_vid = {}
for vid, cyc in enumerate(verts_darts):
    for d in cyc:
        dart_to_vid[d] = vid

# Build faces as triples of vertex ids (one per 3-cycle)
F = []
seen = set()
for cyc in faces_darts:
    tri = tuple(dart_to_vid[d] for d in cyc)
    key = tuple(sorted(tri))
    if len(set(tri))==3 and key not in seen:
        seen.add(key)
        F.append(tri)
assert len(F)==56

# Placeholder coords for 24 vertices (circle)
V = []
R = 0.92
for k in range(24):
    ang = 2*math.pi*k/24.0
    V.append((R*math.cos(ang), R*math.sin(ang), 0.0))

with open("klein_vertices.csv", "w", newline="") as f:
    w=csv.writer(f); w.writerow(["x","y","z"]); w.writerows(V)
with open("klein_faces.csv", "w", newline="") as f:
    w=csv.writer(f); w.writerow(["i","j","k"]); w.writerows(F)

# Print summary
Eset=set()
for a,b,c in F:
    Eset.add(tuple(sorted((a,b))))
    Eset.add(tuple(sorted((b,c))))
    Eset.add(tuple(sorted((c,a))))
print({"V": len(V), "E": len(Eset), "F": len(F), "chi": len(V)-len(Eset)+len(F)})
