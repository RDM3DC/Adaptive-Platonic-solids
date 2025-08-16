# Klein {3,7} generator

This adds a tiny, dependency-free generator for the genus-3 `{3,7}` triangulation.

## Files
- `klein_237_generator.py` – builds the 24-vertex, 56-face mesh and writes `klein_vertices.csv`, `klein_faces.csv`.
- `euler_check_min.py` – quick Euler characteristic check.
- `gb_check_constantK_min.py` – Gauss–Bonnet target for constant K=-1 (area 8π).
- `gb_check_adaptive_min.py` – Gauss–Bonnet check for exported `face_areas.csv` and `K_face.csv`.
- `render_klein_237.py` – one-command demo render producing `outputs/klein_curvature.png`.

## Usage
```bash
python klein_237_generator.py           # emits klein_vertices.csv + klein_faces.csv
python euler_check_min.py klein_vertices.csv klein_faces.csv
python gb_check_constantK_min.py
python render_klein_237.py              # saves face_areas.csv, K_face.csv, outputs/klein_curvature.png
python gb_check_adaptive_min.py face_areas.csv K_face.csv
```

The vertex coordinates are a simple unit-circle layout; topology is exact. For a
faithful hyperbolic embedding, replace them with a Poincaré disk realization.
