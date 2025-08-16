
# Compute Euler characteristic from the 14-gon fundamental domain with opposite-edge pairings.
# Edges: i -> (i+1) mod 14. Pair: i ↔ (i+7) mod 14 (reverse orientation).
# Corners: 0..13. Glue rule from edge pairing identifies corners accordingly.

class DSU:
    def __init__(self, n): self.p=list(range(n))
    def find(self, x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self, a,b):
        ra, rb = self.find(a), self.find(b)
        if ra!=rb: self.p[rb]=ra

N = 14
dsu = DSU(N)

# For edge i=(i, i+1) and its partner j=(i+7) with edge (j, j+1) glued reversed, we identify:
#   corner i   ~ corner j+1
#   corner i+1 ~ corner j
for i in range(N):
    j = (i+7) % N
    dsu.union(i, (j+1)%N)
    dsu.union((i+1)%N, j)

# Count vertex classes
V = len({dsu.find(k) for k in range(N)})
E = N//2    # 14 edges glued in 7 pairs
F = 1       # one fundamental polygon face
chi = V - E + F

print({"V": V, "E": E, "F": F, "chi": chi, "genus": (2-chi)//2})
