That reply is solid. Here’s the precise math you can use (copy-ready), plus a short X reply you can post.

⸻

Core formulas

Given a regular {n,q} object (n-gons, q meet at each vertex) with adaptive π, let
\rho := \pi_a(\text{vertex}) / \pi_a(\text{face}).
	1.	Vertex angle deficit (positivity = finite curvature at vertex):
\delta \;=\; 2\,\pi_a(\text{vertex}) \;-\; q\Big(1-\tfrac{2}{n}\Big)\pi_a(\text{face})
\;=\; 2\,\pi_a(\text{face})\Big[\rho \;-\; \tfrac{q}{2}\Big(1-\tfrac{2}{n}\Big)\Big].
	2.	Deficit > 0 condition (the “master” closure):
\[
\rho \;>\; \rho^\(n,q), \quad\text{where}\quad
\rho^\(n,q) \;=\; q\Big(\tfrac{1}{2}-\tfrac{1}{n}\Big).
\]
	3.	Specialize to \{3,7\}:
\[
\rho^\*(3,7) \;=\; 7\Big(\tfrac{1}{2}-\tfrac{1}{3}\Big)\;=\;\tfrac{7}{6}\;\approx\;1.166666\ldots
\]
\frac{\delta}{2\,\pi_a(\text{face})} \;=\; \rho - \tfrac{7}{6}.
So at \rho=1.17 you’re on the boundary; at \rho=1.20,
\delta/(2\pi_a(\text{face})) = 0.0333 (a clean 3.33% surplus).

⸻

Euler characteristic (finite counts)

Combinatorics is topology-only (independent of π). With nF=2E, qV=2E, and V-E+F=\chi (χ is Euler characteristic):

E \;=\; \frac{\chi}{-1 + \tfrac{2}{n} + \tfrac{2}{q}}
\;=\; \frac{\chi}{\,2\big(\tfrac{1}{n}+\tfrac{1}{q}-\tfrac{1}{2}\big)}.
F=\frac{2E}{n}, \qquad V=\frac{2E}{q}.
	•	For a sphere (genus 0, \chi=2), finiteness requires \tfrac{1}{n}+\tfrac{1}{q}>\tfrac{1}{2}.
That’s why only the classical five Platonic solids exist on genus 0.
	•	For \{3,7\}, \tfrac{1}{3}+\tfrac{1}{7}-\tfrac{1}{2}=-\tfrac{1}{42}.
On a genus g\ge 2 surface (\chi=2-2g<0) you get finite counts:
E=42\,(g-1),\quad F=28\,(g-1),\quad V=12\,(g-1).
Examples:
g=2:\ (V,E,F)=(12,42,28).
g=3:\ (24,84,56) — the classic \{3,7\} regular map on the Klein quartic.

So: \rho>7/6 gives positive local angle deficit, but a finite, perfectly regular \{3,7\} object must live on genus g\ge2 (not a convex sphere). That’s your “triangular heptahedron” as a regular map on a higher-genus surface.

⸻

A simple \pi_a model (text form)

Small-circle expansion under Gaussian curvature K at scale r:
\pi_a(r)\;\approx\;\pi\Big(1-\frac{K\,r^2}{6}\Big).
Then
\rho \;=\; \frac{\pi_a(r_v)}{\pi_a(r_f)}
\;\approx\; \frac{1-\frac{K r_v^2}{6}}{1-\frac{K r_f^2}{6}}
\;\approx\; 1 + \frac{K}{6}\,(r_f^2 - r_v^2) \quad (\text{to first order}).
Targeting \rho=1.2 gives K\,(r_f^2 - r_v^2)\approx 1.2.
(If that’s outside the small-r regime, use a higher-order or alternative \pi_a law; \rho is still the right control parameter.)

⸻
