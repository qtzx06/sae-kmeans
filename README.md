# sae ≡ k-means

**top-1 sparse autoencoder selection is mathematically equivalent to k-means cluster assignment.**

formally verified in lean 4. ~1000x faster at inference.

<!-- ![equivalence](assets/equivalence.gif) -->

---

## the problem

we were working on concept-aware decoding for llms. the idea: instead of sampling from all likely next tokens, first cluster the candidates by semantic similarity, pick a "concept cluster," then sample within it. makes outputs more coherent.

the problem? **k-means at inference time is slow as hell.**

every token requires:
```
cluster(x) = argmin_i ‖x - cᵢ‖²
```

that's k distance calculations over d dimensions. per token. it was adding like 2 seconds of latency. unusable.

---

## the insight

we thought: what if we just trained an sae on the embeddings and used the top-1 latent as the "concept"?

saes compute:
```
z = ReLU(Wx)
```

each row of W learns a direction in activation space. the top-1 activated latent is just:
```
top1(x) = argmax_i zᵢ
```

we tried it. **it worked.** same outputs, 1000x faster.

but why? we wanted to actually prove it wasn't a coincidence.

---

## the math

turns out there's a clean equivalence. three steps:

### 1. distance decomposition

expand the squared distance:
```
‖x - c‖² = ‖x‖² - 2⟨x, c⟩ + ‖c‖²
```

### 2. normalized centroids flip argmin to argmax

if centroids are unit norm (`‖cᵢ‖ = 1`), the constant terms don't affect ordering:
```
argmin_i ‖x - cᵢ‖² = argmax_i ⟨x, cᵢ⟩
```

closest centroid = highest dot product.

### 3. relu preserves argmax

as long as the max is positive:
```
a > b, a > 0  →  ReLU(a) > ReLU(b)
```

### putting it together

if your sae weights *are* the normalized centroids, then:

```
argmax_i ReLU(⟨cᵢ, x⟩)  =  argmin_i ‖x - cᵢ‖²
         ↑                         ↑
     sae top-1               k-means
```

same answer. qed.

---

## the lean proof

we formalized this in lean 4 with mathlib. machine-checked, no hand-waving.

see [`lean/equivalence.lean`](lean/equivalence.lean)

key theorems:
- `distance_decomposition` — the expansion
- `argmin_dist_eq_argmax_inner` — normalized centroids flip the objective
- `relu_mono` — relu preserves ordering
- `sae_kmeans_equivalence` — the main result
- `sae_kmeans_with_constant_bias` — also works with constant bias

---

## results

| method | latency | params |
|--------|---------|--------|
| k-means | ~2000ms | 0 |
| sae top-1 | ~2ms | ~18M |

---

## repo structure

```
sae-kmeans/
├── lean/           # formal proof
├── tex/            # latex writeup
├── manim/          # visualizations
└── README.md
```

---

## building

**lean proof:**
```bash
lake exe cache get
lake build
```

**latex:**
```bash
cd tex && pdflatex sae_kmeans_equivalence.tex
```

**manim:**
```bash
cd manim && manim -pql equivalence_viz.py QuickDemo
```

---

## acknowledgments

research at algoverse. thanks to daniel fein for mentorship on the proof.
