/-
  SAE-KMeans Equivalence Proof

  This file proves the mathematical equivalence between:
  1. Top-1 Sparse Autoencoder (SAE) latent selection
  2. k-means cluster assignment

  Under the conditions that:
  - Centroids are normalized (unit norm)
  - SAE encoder weights equal the centroids
  - SAE bias is zero (or constant)
  - At least one dot product is positive
-/

import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.Basic

open scoped InnerProductSpace
open BigOperators

variable {d : ℕ}
variable {k : ℕ}

noncomputable def relu : ℝ → ℝ := fun t => max 0 t

theorem distance_decomposition {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x c : E) : ‖x - c‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, c⟫_ℝ + ‖c‖ ^ 2 := by
  rw [norm_sub_sq_real]

theorem distance_normalized {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x c : E) (hc : ‖c‖ = 1) : ‖x - c‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, c⟫_ℝ + 1 := by
  rw [distance_decomposition]
  simp only [hc, one_pow]

theorem argmin_dist_eq_argmax_inner
    (centroids : Fin k → EuclideanSpace ℝ (Fin d))
    (x : EuclideanSpace ℝ (Fin d))
    (h_normalized : ∀ i, ‖centroids i‖ = 1)
    (i_star : Fin k)
    (h_min : ∀ j, ‖x - centroids i_star‖ ^ 2 ≤ ‖x - centroids j‖ ^ 2) :
    ∀ j, ⟪centroids i_star, x⟫_ℝ ≥ ⟪centroids j, x⟫_ℝ := by
  intro j
  have h1 : ‖x - centroids i_star‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids i_star⟫_ℝ + 1 :=
    distance_normalized x (centroids i_star) (h_normalized i_star)
  have h2 : ‖x - centroids j‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids j⟫_ℝ + 1 :=
    distance_normalized x (centroids j) (h_normalized j)
  have h3 := h_min j
  rw [h1, h2] at h3
  have sym1 : ⟪centroids i_star, x⟫_ℝ = ⟪x, centroids i_star⟫_ℝ := real_inner_comm _ _
  have sym2 : ⟪centroids j, x⟫_ℝ = ⟪x, centroids j⟫_ℝ := real_inner_comm _ _
  rw [sym1, sym2]
  linarith

theorem relu_nonneg (t : ℝ) : 0 ≤ relu t := le_max_left 0 t

theorem relu_of_pos {t : ℝ} (h : 0 < t) : relu t = t := max_eq_right_of_lt h

theorem relu_of_nonpos {t : ℝ} (h : t ≤ 0) : relu t = 0 := max_eq_left h

theorem relu_strict_mono {a b : ℝ} (hab : a > b) (ha_pos : a > 0) : relu a > relu b := by
  rw [relu_of_pos ha_pos]
  rcases le_or_gt b 0 with hb | hb
  · rw [relu_of_nonpos hb]
    exact ha_pos
  · rw [relu_of_pos hb]
    exact hab

theorem relu_mono {a b : ℝ} (hab : a ≥ b) (ha_pos : a > 0) : relu a ≥ relu b := by
  rcases eq_or_lt_of_le hab with rfl | h
  · rfl
  · exact le_of_lt (relu_strict_mono h ha_pos)

theorem sae_kmeans_equivalence
    (centroids : Fin k → EuclideanSpace ℝ (Fin d))
    (x : EuclideanSpace ℝ (Fin d))
    (h_normalized : ∀ i, ‖centroids i‖ = 1)
    (i_star : Fin k)
    (h_max_inner : ∀ j, ⟪centroids i_star, x⟫_ℝ ≥ ⟪centroids j, x⟫_ℝ)
    (h_pos : ⟪centroids i_star, x⟫_ℝ > 0) :
    (∀ j, relu ⟪centroids i_star, x⟫_ℝ ≥ relu ⟪centroids j, x⟫_ℝ) ∧
    (∀ j, ‖x - centroids i_star‖ ^ 2 ≤ ‖x - centroids j‖ ^ 2) := by
  constructor
  · intro j
    exact relu_mono (h_max_inner j) h_pos
  · intro j
    have h1 : ‖x - centroids i_star‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids i_star⟫_ℝ + 1 :=
      distance_normalized x (centroids i_star) (h_normalized i_star)
    have h2 : ‖x - centroids j‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids j⟫_ℝ + 1 :=
      distance_normalized x (centroids j) (h_normalized j)
    rw [h1, h2]
    have sym1 : ⟪centroids i_star, x⟫_ℝ = ⟪x, centroids i_star⟫_ℝ := real_inner_comm _ _
    have sym2 : ⟪centroids j, x⟫_ℝ = ⟪x, centroids j⟫_ℝ := real_inner_comm _ _
    have h3 : ⟪x, centroids i_star⟫_ℝ ≥ ⟪x, centroids j⟫_ℝ := by
      rw [← sym1, ← sym2]
      exact h_max_inner j
    linarith

theorem constant_bias_preserves_argmax
    (f : Fin k → ℝ) (β : ℝ) (i_star : Fin k)
    (h_max : ∀ j, f i_star ≥ f j) :
    ∀ j, f i_star + β ≥ f j + β := by
  intro j
  linarith [h_max j]

theorem sae_kmeans_with_constant_bias
    (centroids : Fin k → EuclideanSpace ℝ (Fin d))
    (x : EuclideanSpace ℝ (Fin d))
    (β : ℝ) -- constant bias
    (h_normalized : ∀ i, ‖centroids i‖ = 1)
    (i_star : Fin k)
    (h_max_inner : ∀ j, ⟪centroids i_star, x⟫_ℝ ≥ ⟪centroids j, x⟫_ℝ)
    (h_pos : ⟪centroids i_star, x⟫_ℝ + β > 0) :
    (∀ j, relu (⟪centroids i_star, x⟫_ℝ + β) ≥ relu (⟪centroids j, x⟫_ℝ + β)) ∧
    (∀ j, ‖x - centroids i_star‖ ^ 2 ≤ ‖x - centroids j‖ ^ 2) := by
  constructor
  · intro j
    have h_shifted : ⟪centroids i_star, x⟫_ℝ + β ≥ ⟪centroids j, x⟫_ℝ + β := by
      linarith [h_max_inner j]
    exact relu_mono h_shifted h_pos
  · intro j
    have h1 : ‖x - centroids i_star‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids i_star⟫_ℝ + 1 :=
      distance_normalized x (centroids i_star) (h_normalized i_star)
    have h2 : ‖x - centroids j‖ ^ 2 = ‖x‖ ^ 2 - 2 * ⟪x, centroids j⟫_ℝ + 1 :=
      distance_normalized x (centroids j) (h_normalized j)
    rw [h1, h2]
    have sym1 : ⟪centroids i_star, x⟫_ℝ = ⟪x, centroids i_star⟫_ℝ := real_inner_comm _ _
    have sym2 : ⟪centroids j, x⟫_ℝ = ⟪x, centroids j⟫_ℝ := real_inner_comm _ _
    have h3 : ⟪x, centroids i_star⟫_ℝ ≥ ⟪x, centroids j⟫_ℝ := by
      rw [← sym1, ← sym2]
      exact h_max_inner j
    linarith
