"""
SAE ≡ K-Means Equivalence Visualization
"""

from manim import *
import numpy as np

# === COLOR PALETTE (white bg, greyscale + blue/orange accents) ===
BACKGROUND = "#ffffff"
TEXT_PRIMARY = "#1a1a1a"
TEXT_SECONDARY = "#666666"

BLUE = "#165A95"
ORANGE = "#ea580c"
GREY_DARK = "#404040"
GREY_MID = "#808080"
GREY_LIGHT = "#b3b3b3"

# Centroid colors (blue primary, grey for others)
C1_COLOR = BLUE
C2_COLOR = GREY_MID
C3_COLOR = GREY_LIGHT

# Point color (orange accent)
POINT_COLOR = ORANGE


class SAEKMeansEquivalence(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.intro()
        self.kmeans_scene()
        self.sae_scene()
        self.equivalence_scene()
        self.math_scene()
        self.outro()

    def intro(self):
        """Title and hook"""
        title = Text("SAE ≡ K-Means", font_size=56, color=TEXT_PRIMARY)

        self.play(Write(title), run_time=1.5)
        self.wait(1)

        subtitle = Text(
            "a formal equivalence",
            font_size=28,
            color=TEXT_SECONDARY
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        self.play(
            FadeOut(title, shift=UP * 0.5),
            FadeOut(subtitle, shift=UP * 0.5),
            run_time=0.8
        )
        self.wait(0.3)

    def kmeans_scene(self):
        """Visualize k-means clustering"""
        # Section label
        label = Text("k-means clustering", font_size=32, color=TEXT_SECONDARY)
        label.to_edge(UP, buff=0.5)
        self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.6)

        # Create axes (subtle, not prominent)
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            tips=False,
            axis_config={
                "stroke_color": TEXT_SECONDARY,
                "stroke_opacity": 0.3,
                "stroke_width": 1,
            }
        )
        axes.shift(LEFT * 2.5)

        # Unit circle (very subtle)
        circle = Circle(radius=axes.x_length / 5, color=TEXT_SECONDARY, stroke_opacity=0.2)
        circle.move_to(axes.c2p(0, 0))

        self.play(Create(axes, run_time=0.8), Create(circle, run_time=0.8))

        # Centroids (normalized, on unit circle)
        centroid_positions = [
            (1, 0),           # c1: right
            (-0.5, 0.866),    # c2: upper left
            (-0.5, -0.866),   # c3: lower left
        ]
        centroid_colors = [C1_COLOR, C2_COLOR, C3_COLOR]
        centroid_label_dirs = [RIGHT, UL, DL]

        centroids = VGroup()
        centroid_labels = VGroup()

        for i, (pos, col, ldir) in enumerate(zip(centroid_positions, centroid_colors, centroid_label_dirs)):
            # Centroid dot with glow effect
            glow = Dot(
                axes.c2p(pos[0], pos[1]),
                radius=0.18,
                color=col,
                fill_opacity=0.3
            )
            dot = Dot(
                axes.c2p(pos[0], pos[1]),
                radius=0.12,
                color=col,
                fill_opacity=1
            )
            centroid = VGroup(glow, dot)
            centroids.add(centroid)

            # Label
            label_text = MathTex(f"c_{i+1}", font_size=24, color=col)
            label_text.next_to(dot, ldir, buff=0.15)
            centroid_labels.add(label_text)

        self.play(
            *[GrowFromCenter(c, run_time=0.6) for c in centroids],
            lag_ratio=0.15
        )
        self.play(
            *[FadeIn(l, shift=UP * 0.1) for l in centroid_labels],
            lag_ratio=0.1,
            run_time=0.5
        )
        self.wait(0.5)

        # Query point x
        x_pos = np.array([0.5, 0.4])
        x_glow = Dot(axes.c2p(x_pos[0], x_pos[1]), radius=0.14, color=POINT_COLOR, fill_opacity=0.3)
        x_dot = Dot(axes.c2p(x_pos[0], x_pos[1]), radius=0.09, color=POINT_COLOR)
        x_point = VGroup(x_glow, x_dot)
        x_label = MathTex("x", font_size=26, color=POINT_COLOR)
        x_label.next_to(x_dot, UR, buff=0.1)

        self.play(GrowFromCenter(x_point), FadeIn(x_label, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)

        # Draw distance lines
        dist_lines = VGroup()
        for i, (pos, col) in enumerate(zip(centroid_positions, centroid_colors)):
            line = DashedLine(
                axes.c2p(x_pos[0], x_pos[1]),
                axes.c2p(pos[0], pos[1]),
                color=col,
                stroke_opacity=0.5,
                stroke_width=2,
                dash_length=0.08
            )
            dist_lines.add(line)

        self.play(
            *[Create(line) for line in dist_lines],
            lag_ratio=0.1,
            run_time=0.8
        )
        self.wait(0.3)

        # Formula on the right
        formula = MathTex(
            r"\text{cluster}(x) = \arg\min_i \|x - c_i\|^2",
            font_size=26,
            color=TEXT_PRIMARY
        )
        formula.to_edge(RIGHT, buff=0.8).shift(UP * 1.5)

        self.play(Write(formula), run_time=1)
        self.wait(0.5)

        # Highlight the closest (c1)
        self.play(
            dist_lines[0].animate.set_stroke(opacity=1, width=3),
            dist_lines[1].animate.set_stroke(opacity=0.15),
            dist_lines[2].animate.set_stroke(opacity=0.15),
            run_time=0.6
        )

        result = MathTex(r"= c_1", font_size=26, color=C1_COLOR)
        result.next_to(formula, DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(Write(result), run_time=0.5)
        self.wait(1)

        # Store for later
        self.kmeans_group = VGroup(
            axes, circle, centroids, centroid_labels,
            x_point, x_label, dist_lines, formula, result, label
        )

        # Fade out
        self.play(FadeOut(self.kmeans_group), run_time=0.8)
        self.wait(0.3)

    def sae_scene(self):
        """Visualize SAE encoding and top-1 selection"""
        # Section label
        label = Text("sparse autoencoder", font_size=32, color=TEXT_SECONDARY)
        label.to_edge(UP, buff=0.5)
        self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.6)

        # Input vector x
        x_box = Rectangle(
            width=0.6, height=1.8,
            color=POINT_COLOR,
            fill_opacity=0.15,
            stroke_width=2
        )
        x_box.shift(LEFT * 4.5)
        x_label = MathTex("x", font_size=28, color=POINT_COLOR)
        x_label.next_to(x_box, DOWN, buff=0.2)

        self.play(
            Create(x_box),
            FadeIn(x_label, shift=UP * 0.1),
            run_time=0.6
        )

        # Weight matrix W
        w_box = Rectangle(
            width=1.8, height=1.8,
            color=TEXT_PRIMARY,
            fill_opacity=0.1,
            stroke_width=2,
            stroke_opacity=0.8
        )
        w_box.shift(LEFT * 1.5)
        w_label = MathTex("W", font_size=28, color=TEXT_PRIMARY)
        w_label.move_to(w_box)

        # Arrow from x to W
        arrow1 = Arrow(
            x_box.get_right(),
            w_box.get_left(),
            buff=0.15,
            color=TEXT_SECONDARY,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            GrowArrow(arrow1),
            Create(w_box),
            FadeIn(w_label),
            run_time=0.7
        )

        # ReLU box
        relu_box = Rectangle(
            width=1.2, height=1.2,
            color=ORANGE,
            fill_opacity=0.15,
            stroke_width=2
        )
        relu_box.shift(RIGHT * 1)
        relu_label = Text("ReLU", font_size=20, color=ORANGE)
        relu_label.move_to(relu_box)

        arrow2 = Arrow(
            w_box.get_right(),
            relu_box.get_left(),
            buff=0.15,
            color=TEXT_SECONDARY,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            GrowArrow(arrow2),
            Create(relu_box),
            FadeIn(relu_label),
            run_time=0.7
        )

        # Output activations z (as bars)
        z_group = VGroup()
        bar_colors = [C1_COLOR, C2_COLOR, C3_COLOR]
        bar_heights = [0.9, 0.3, 0.15]  # c1 is highest

        for i, (col, h) in enumerate(zip(bar_colors, bar_heights)):
            bar = Rectangle(
                width=0.35,
                height=h * 1.5,
                color=col,
                fill_opacity=0.7,
                stroke_width=1
            )
            bar.move_to(RIGHT * 3.5 + UP * (h * 0.75 - 0.5) + RIGHT * (i - 1) * 0.5)
            z_group.add(bar)

        z_label = MathTex("z", font_size=28, color=TEXT_PRIMARY)
        z_label.next_to(z_group, DOWN, buff=0.3)

        arrow3 = Arrow(
            relu_box.get_right(),
            z_group.get_left(),
            buff=0.15,
            color=TEXT_SECONDARY,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(GrowArrow(arrow3), run_time=0.5)
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in z_group],
            FadeIn(z_label, shift=UP * 0.1),
            lag_ratio=0.1,
            run_time=0.8
        )
        self.wait(0.5)

        # Formula
        formula = MathTex(
            r"z = \text{ReLU}(Wx)",
            font_size=26,
            color=TEXT_PRIMARY
        )
        formula.to_edge(DOWN, buff=1.2)

        self.play(Write(formula), run_time=0.8)
        self.wait(0.3)

        # Top-1 selection
        top1_formula = MathTex(
            r"\text{top}_1(x) = \arg\max_i \, z_i",
            font_size=26,
            color=TEXT_PRIMARY
        )
        top1_formula.next_to(formula, DOWN, buff=0.3)

        self.play(Write(top1_formula), run_time=0.8)

        # Highlight the tallest bar
        highlight_box = SurroundingRectangle(
            z_group[0],
            color=POINT_COLOR,
            buff=0.08,
            stroke_width=2
        )

        result = MathTex(r"= z_1", font_size=26, color=C1_COLOR)
        result.next_to(top1_formula, RIGHT, buff=0.3)

        self.play(Create(highlight_box), Write(result), run_time=0.6)
        self.wait(1)

        # Store and fade out
        self.sae_group = VGroup(
            x_box, x_label, arrow1, w_box, w_label, arrow2,
            relu_box, relu_label, arrow3, z_group, z_label,
            formula, top1_formula, result, highlight_box, label
        )

        self.play(FadeOut(self.sae_group), run_time=0.8)
        self.wait(0.3)

    def equivalence_scene(self):
        """Show both methods select the same index - structural parallel"""
        # Section label
        label = Text("the equivalence", font_size=32, color=TEXT_SECONDARY)
        label.to_edge(UP, buff=0.5)
        self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.6)

        # === LEFT SIDE: K-MEANS ===
        kmeans_title = Text("k-means", font_size=22, color=BLUE)
        kmeans_title.shift(LEFT * 3.5 + UP * 2)

        # Small coordinate system with centroids
        km_axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.5,
            y_length=2.5,
            tips=False,
            axis_config={
                "stroke_color": TEXT_SECONDARY,
                "stroke_opacity": 0.2,
                "stroke_width": 1,
            }
        )
        km_axes.shift(LEFT * 3.5 + DOWN * 0.3)

        # Centroids (2D positions for axes)
        centroid_positions_2d = [
            (1, 0),
            (-0.5, 0.866),
            (-0.5, -0.866),
        ]
        centroid_colors = [C1_COLOR, C2_COLOR, C3_COLOR]

        km_centroids = VGroup()
        km_labels = VGroup()
        label_dirs = [RIGHT, UL, DL]  # directions for labels
        for i, (pos, col, ldir) in enumerate(zip(centroid_positions_2d, centroid_colors, label_dirs)):
            dot = Dot(km_axes.c2p(pos[0], pos[1]), radius=0.08, color=col)
            km_centroids.add(dot)
            lbl = MathTex(f"c_{i+1}", font_size=18, color=col)
            lbl.next_to(dot, ldir, buff=0.08)
            km_labels.add(lbl)

        # Query point
        x_pos = (0.4, 0.3)
        km_x = Dot(km_axes.c2p(x_pos[0], x_pos[1]), radius=0.06, color=POINT_COLOR)
        km_x_label = MathTex("x", font_size=18, color=POINT_COLOR)
        km_x_label.next_to(km_x, UR, buff=0.05)

        # Distance line to nearest (c1)
        km_dist_line = Line(
            km_axes.c2p(x_pos[0], x_pos[1]),
            km_axes.c2p(centroid_positions_2d[0][0], centroid_positions_2d[0][1]),
            color=C1_COLOR,
            stroke_width=2
        )

        self.play(
            FadeIn(kmeans_title, shift=DOWN * 0.1),
            Create(km_axes),
            run_time=0.6
        )
        self.play(
            *[GrowFromCenter(c) for c in km_centroids],
            *[FadeIn(l) for l in km_labels],
            run_time=0.5
        )
        self.play(
            GrowFromCenter(km_x),
            FadeIn(km_x_label),
            run_time=0.4
        )
        self.play(Create(km_dist_line), run_time=0.4)

        # === RIGHT SIDE: SAE ===
        sae_title = Text("SAE", font_size=22, color=BLUE)
        sae_title.shift(RIGHT * 3.5 + UP * 2)

        # Sparse activation vector (vertical bars)
        # Most are zero (gray), one is active (colored)
        sae_bars = VGroup()
        bar_x_start = RIGHT * 2.2
        bar_width = 0.25
        bar_spacing = 0.35

        # Values: mostly 0, neuron 1 active
        activations = [0.85, 0.0, 0.0, 0.0, 0.0]  # first neuron active
        neuron_colors = [C1_COLOR, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY]

        for i, (val, col) in enumerate(zip(activations, neuron_colors)):
            if val > 0:
                bar = Rectangle(
                    width=bar_width,
                    height=val * 1.5,
                    color=col,
                    fill_opacity=0.8,
                    stroke_width=1
                )
            else:
                # Empty/zero bar
                bar = Rectangle(
                    width=bar_width,
                    height=0.08,
                    color=TEXT_SECONDARY,
                    fill_opacity=0.3,
                    stroke_width=1
                )
            bar.move_to(bar_x_start + RIGHT * i * bar_spacing + DOWN * 0.3)
            bar.align_to(bar_x_start + DOWN * 1, DOWN)
            sae_bars.add(bar)

        # Label for z
        z_label = MathTex("z", font_size=22, color=TEXT_PRIMARY)
        z_label.next_to(sae_bars, DOWN, buff=0.25)

        # Neuron labels
        neuron_labels = VGroup()
        for i in range(5):
            if i < 3:
                nl = MathTex(f"z_{i+1}", font_size=14, color=neuron_colors[i])
            else:
                nl = MathTex(r"\cdots", font_size=14, color=TEXT_SECONDARY)
            nl.next_to(sae_bars[i], UP, buff=0.1)
            neuron_labels.add(nl)

        self.play(
            FadeIn(sae_title, shift=DOWN * 0.1),
            run_time=0.4
        )
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in sae_bars],
            lag_ratio=0.05,
            run_time=0.6
        )
        self.play(
            FadeIn(z_label),
            *[FadeIn(nl) for nl in neuron_labels[:3]],
            run_time=0.4
        )

        # === CONNECTING ARROW: active neuron → centroid ===
        # Show that z_1 (active neuron) corresponds to c_1 (nearest centroid)

        # Highlight the active neuron
        active_highlight = SurroundingRectangle(
            sae_bars[0],
            color=POINT_COLOR,
            buff=0.05,
            stroke_width=2
        )

        # Highlight the winning centroid
        centroid_highlight = Circle(
            radius=0.15,
            color=POINT_COLOR,
            stroke_width=2
        )
        centroid_highlight.move_to(km_centroids[0])

        self.play(
            Create(active_highlight),
            Create(centroid_highlight),
            run_time=0.5
        )

        # Curved arrow connecting them
        connect_arrow = CurvedArrow(
            sae_bars[0].get_left() + LEFT * 0.1,
            km_centroids[0].get_right() + RIGHT * 0.2,
            color=POINT_COLOR,
            stroke_width=2,
            angle=-TAU/4,
            tip_length=0.15
        )

        self.play(Create(connect_arrow), run_time=0.6)

        # Label: "same selection"
        same_label = Text("same selection", font_size=18, color=POINT_COLOR)
        same_label.next_to(connect_arrow, UP, buff=0.15)

        self.play(FadeIn(same_label, shift=DOWN * 0.1), run_time=0.4)
        self.wait(0.5)

        # === EQUATIONS AT BOTTOM ===
        km_eq = MathTex(
            r"\arg\min_i \|x - c_i\|^2",
            font_size=22,
            color=BLUE
        )
        km_eq.shift(LEFT * 3.5 + DOWN * 2.3)

        sae_eq = MathTex(
            r"\arg\max_i \, z_i",
            font_size=22,
            color=BLUE
        )
        sae_eq.shift(RIGHT * 3.5 + DOWN * 2.3)

        equals = MathTex(r"=", font_size=32, color=POINT_COLOR)
        equals.move_to(DOWN * 2.3)

        self.play(
            Write(km_eq),
            Write(sae_eq),
            run_time=0.6
        )
        self.play(Write(equals), run_time=0.4)

        self.wait(1.5)

        # Fade out
        self.equiv_group = VGroup(
            label, kmeans_title, km_axes, km_centroids, km_labels,
            km_x, km_x_label, km_dist_line,
            sae_title, sae_bars, z_label, neuron_labels,
            active_highlight, centroid_highlight, connect_arrow, same_label,
            km_eq, sae_eq, equals
        )

        self.play(FadeOut(self.equiv_group), run_time=0.8)
        self.wait(0.3)

    def math_scene(self):
        """Step through the mathematical proof"""
        # Section label
        label = Text("the proof", font_size=32, color=TEXT_SECONDARY)
        label.to_edge(UP, buff=0.5)
        self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.6)

        # Step 1: Distance decomposition
        step1_label = Text("1. expand the distance", font_size=20, color=TEXT_SECONDARY)
        step1_label.shift(UP * 2 + LEFT * 3)

        step1 = MathTex(
            r"\|x - c\|^2",
            r"=",
            r"\|x\|^2 - 2\langle x, c \rangle + \|c\|^2",
            font_size=26
        )
        step1[0].set_color(TEXT_PRIMARY)
        step1[2].set_color(TEXT_PRIMARY)
        step1.next_to(step1_label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(FadeIn(step1_label, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Write(step1[0]), run_time=0.5)
        self.wait(0.2)
        self.play(Write(step1[1:]), run_time=0.8)
        self.wait(0.5)

        # Step 2: Normalized centroids
        step2_label = Text("2. if centroids are normalized", font_size=20, color=TEXT_SECONDARY)
        step2_label.shift(UP * 0.3 + LEFT * 3)

        step2a = MathTex(
            r"\|c_i\| = 1",
            font_size=26,
            color=BLUE
        )
        step2a.next_to(step2_label, DOWN, buff=0.3, aligned_edge=LEFT)

        step2b = MathTex(
            r"\Rightarrow \arg\min_i \|x - c_i\|^2 = \arg\max_i \langle x, c_i \rangle",
            font_size=24,
            color=TEXT_PRIMARY
        )
        step2b.next_to(step2a, DOWN, buff=0.25, aligned_edge=LEFT)

        self.play(FadeIn(step2_label, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Write(step2a), run_time=0.5)
        self.wait(0.2)
        self.play(Write(step2b), run_time=0.8)
        self.wait(0.5)

        # Step 3: ReLU preserves argmax
        step3_label = Text("3. ReLU preserves ordering", font_size=20, color=TEXT_SECONDARY)
        step3_label.shift(DOWN * 1.5 + LEFT * 3)

        step3 = MathTex(
            r"a > b, \, a > 0 \;\Rightarrow\; \text{ReLU}(a) > \text{ReLU}(b)",
            font_size=24,
            color=TEXT_PRIMARY
        )
        step3.next_to(step3_label, DOWN, buff=0.3, aligned_edge=LEFT)

        # ReLU image on the right
        relu_img = ImageMobject("/home/qtzx/Codebase/sae-kmeans/assets/relu.png")
        relu_img.scale(0.7)
        relu_img.shift(RIGHT * 4 + DOWN * 0.3)

        self.play(FadeIn(step3_label, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Write(step3), FadeIn(relu_img, shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.8)

        # QED
        qed = MathTex(
            r"\therefore \quad \text{SAE top-1} = \text{k-means}",
            font_size=28,
            color=BLUE
        )
        qed.shift(DOWN * 2.8)

        qed_box = SurroundingRectangle(qed, color=BLUE, buff=0.2, stroke_width=2)

        self.play(Write(qed), run_time=0.8)
        self.play(Create(qed_box), run_time=0.5)
        self.wait(1.5)

        # Fade out
        self.math_group = Group(
            label, step1_label, step1, step2_label, step2a, step2b,
            step3_label, step3, qed, qed_box, relu_img
        )

        self.play(FadeOut(self.math_group), run_time=0.8)
        self.wait(0.3)

    def outro(self):
        """Closing"""
        line1 = Text("formally verified in Lean 4", font_size=28, color=TEXT_PRIMARY)

        self.play(Write(line1), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(line1), run_time=0.8)
        self.wait(0.5)


# === INDIVIDUAL SCENES FOR GIF EXPORT ===

class KMeansScene(Scene):
    """K-means clustering visualization - for README section"""
    def construct(self):
        self.camera.background_color = BACKGROUND

        # Create axes
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            tips=False,
            axis_config={
                "stroke_color": TEXT_SECONDARY,
                "stroke_opacity": 0.3,
                "stroke_width": 1,
            }
        )

        # Unit circle
        circle = Circle(radius=axes.x_length / 5, color=TEXT_SECONDARY, stroke_opacity=0.2)
        circle.move_to(axes.c2p(0, 0))

        self.play(Create(axes, run_time=0.6), Create(circle, run_time=0.6))

        # Centroids
        centroid_positions = [
            (1, 0),
            (-0.5, 0.866),
            (-0.5, -0.866),
        ]
        centroid_colors = [C1_COLOR, C2_COLOR, C3_COLOR]
        centroid_label_dirs = [RIGHT, UL, DL]

        centroids = VGroup()
        centroid_labels = VGroup()

        for i, (pos, col, ldir) in enumerate(zip(centroid_positions, centroid_colors, centroid_label_dirs)):
            glow = Dot(axes.c2p(pos[0], pos[1]), radius=0.18, color=col, fill_opacity=0.3)
            dot = Dot(axes.c2p(pos[0], pos[1]), radius=0.12, color=col, fill_opacity=1)
            centroid = VGroup(glow, dot)
            centroids.add(centroid)

            label_text = MathTex(f"c_{i+1}", font_size=24, color=col)
            label_text.next_to(dot, ldir, buff=0.15)
            centroid_labels.add(label_text)

        self.play(
            *[GrowFromCenter(c, run_time=0.5) for c in centroids],
            lag_ratio=0.1
        )
        self.play(
            *[FadeIn(l, shift=UP * 0.1) for l in centroid_labels],
            lag_ratio=0.1,
            run_time=0.4
        )

        # Query point x
        x_pos = np.array([0.5, 0.4])
        x_glow = Dot(axes.c2p(x_pos[0], x_pos[1]), radius=0.14, color=POINT_COLOR, fill_opacity=0.3)
        x_dot = Dot(axes.c2p(x_pos[0], x_pos[1]), radius=0.09, color=POINT_COLOR)
        x_point = VGroup(x_glow, x_dot)
        x_label = MathTex("x", font_size=26, color=POINT_COLOR)
        x_label.next_to(x_dot, UR, buff=0.1)

        self.play(GrowFromCenter(x_point), FadeIn(x_label, shift=UP * 0.1), run_time=0.5)

        # Distance lines
        dist_lines = VGroup()
        for i, (pos, col) in enumerate(zip(centroid_positions, centroid_colors)):
            line = DashedLine(
                axes.c2p(x_pos[0], x_pos[1]),
                axes.c2p(pos[0], pos[1]),
                color=col,
                stroke_opacity=0.5,
                stroke_width=2,
                dash_length=0.08
            )
            dist_lines.add(line)

        self.play(
            *[Create(line) for line in dist_lines],
            lag_ratio=0.1,
            run_time=0.6
        )

        # Formula
        formula = MathTex(
            r"\text{cluster}(x) = \arg\min_i \|x - c_i\|^2",
            font_size=24,
            color=TEXT_PRIMARY
        )
        formula.to_edge(DOWN, buff=0.8)

        self.play(Write(formula), run_time=0.8)

        # Highlight closest
        self.play(
            dist_lines[0].animate.set_stroke(opacity=1, width=3),
            dist_lines[1].animate.set_stroke(opacity=0.15),
            dist_lines[2].animate.set_stroke(opacity=0.15),
            run_time=0.5
        )

        result = MathTex(r"= c_1", font_size=24, color=C1_COLOR)
        result.next_to(formula, RIGHT, buff=0.2)

        self.play(Write(result), run_time=0.4)
        self.wait(1)


class SAEScene(Scene):
    """SAE encoding visualization - for README section"""
    def construct(self):
        self.camera.background_color = BACKGROUND

        # Input vector x
        x_box = Rectangle(
            width=0.6, height=1.8,
            color=POINT_COLOR,
            fill_opacity=0.15,
            stroke_width=2
        )
        x_box.shift(LEFT * 4)
        x_label = MathTex("x", font_size=28, color=POINT_COLOR)
        x_label.next_to(x_box, DOWN, buff=0.2)

        self.play(Create(x_box), FadeIn(x_label, shift=UP * 0.1), run_time=0.5)

        # Weight matrix W
        w_box = Rectangle(
            width=1.8, height=1.8,
            color=TEXT_PRIMARY,
            fill_opacity=0.1,
            stroke_width=2,
            stroke_opacity=0.8
        )
        w_box.shift(LEFT * 1)
        w_label = MathTex("W", font_size=28, color=TEXT_PRIMARY)
        w_label.move_to(w_box)

        arrow1 = Arrow(
            x_box.get_right(), w_box.get_left(),
            buff=0.15, color=TEXT_SECONDARY, stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(GrowArrow(arrow1), Create(w_box), FadeIn(w_label), run_time=0.6)

        # ReLU box
        relu_box = Rectangle(
            width=1.2, height=1.2,
            color=ORANGE,
            fill_opacity=0.15,
            stroke_width=2
        )
        relu_box.shift(RIGHT * 1.5)
        relu_label = Text("ReLU", font_size=20, color=ORANGE)
        relu_label.move_to(relu_box)

        arrow2 = Arrow(
            w_box.get_right(), relu_box.get_left(),
            buff=0.15, color=TEXT_SECONDARY, stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(GrowArrow(arrow2), Create(relu_box), FadeIn(relu_label), run_time=0.6)

        # Output activations z (as bars)
        z_group = VGroup()
        bar_colors = [C1_COLOR, C2_COLOR, C3_COLOR]
        bar_heights = [0.9, 0.3, 0.15]

        for i, (col, h) in enumerate(zip(bar_colors, bar_heights)):
            bar = Rectangle(
                width=0.35, height=h * 1.5,
                color=col, fill_opacity=0.7, stroke_width=1
            )
            bar.move_to(RIGHT * 4 + UP * (h * 0.75 - 0.5) + RIGHT * (i - 1) * 0.5)
            z_group.add(bar)

        z_label = MathTex("z", font_size=28, color=TEXT_PRIMARY)
        z_label.next_to(z_group, DOWN, buff=0.3)

        arrow3 = Arrow(
            relu_box.get_right(), z_group.get_left(),
            buff=0.15, color=TEXT_SECONDARY, stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(GrowArrow(arrow3), run_time=0.4)
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in z_group],
            FadeIn(z_label, shift=UP * 0.1),
            lag_ratio=0.1,
            run_time=0.6
        )

        # Formula
        formula = MathTex(r"z = \text{ReLU}(Wx)", font_size=24, color=TEXT_PRIMARY)
        formula.to_edge(DOWN, buff=1)

        self.play(Write(formula), run_time=0.6)

        # Top-1 selection
        top1_formula = MathTex(r"\text{top}_1(x) = \arg\max_i \, z_i", font_size=24, color=TEXT_PRIMARY)
        top1_formula.next_to(formula, DOWN, buff=0.25)

        self.play(Write(top1_formula), run_time=0.6)

        # Highlight tallest bar
        highlight_box = SurroundingRectangle(z_group[0], color=POINT_COLOR, buff=0.08, stroke_width=2)
        result = MathTex(r"= z_1", font_size=24, color=C1_COLOR)
        result.next_to(top1_formula, RIGHT, buff=0.2)

        self.play(Create(highlight_box), Write(result), run_time=0.5)
        self.wait(1)


class EquivalenceScene(Scene):
    """Side-by-side equivalence visualization - for README section"""
    def construct(self):
        self.camera.background_color = BACKGROUND

        # === LEFT SIDE: K-MEANS ===
        kmeans_title = Text("k-means", font_size=22, color=BLUE)
        kmeans_title.shift(LEFT * 3.5 + UP * 2.3)

        km_axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.5,
            y_length=2.5,
            tips=False,
            axis_config={"stroke_color": TEXT_SECONDARY, "stroke_opacity": 0.2, "stroke_width": 1}
        )
        km_axes.shift(LEFT * 3.5)

        centroid_positions_2d = [(1, 0), (-0.5, 0.866), (-0.5, -0.866)]
        centroid_colors = [C1_COLOR, C2_COLOR, C3_COLOR]
        label_dirs = [RIGHT, UL, DL]

        km_centroids = VGroup()
        km_labels = VGroup()
        for i, (pos, col, ldir) in enumerate(zip(centroid_positions_2d, centroid_colors, label_dirs)):
            dot = Dot(km_axes.c2p(pos[0], pos[1]), radius=0.08, color=col)
            km_centroids.add(dot)
            lbl = MathTex(f"c_{i+1}", font_size=18, color=col)
            lbl.next_to(dot, ldir, buff=0.08)
            km_labels.add(lbl)

        x_pos = (0.4, 0.3)
        km_x = Dot(km_axes.c2p(x_pos[0], x_pos[1]), radius=0.06, color=POINT_COLOR)
        km_x_label = MathTex("x", font_size=18, color=POINT_COLOR)
        km_x_label.next_to(km_x, UR, buff=0.05)

        km_dist_line = Line(
            km_axes.c2p(x_pos[0], x_pos[1]),
            km_axes.c2p(centroid_positions_2d[0][0], centroid_positions_2d[0][1]),
            color=C1_COLOR, stroke_width=2
        )

        self.play(
            FadeIn(kmeans_title, shift=DOWN * 0.1),
            Create(km_axes),
            run_time=0.5
        )
        self.play(
            *[GrowFromCenter(c) for c in km_centroids],
            *[FadeIn(l) for l in km_labels],
            run_time=0.4
        )
        self.play(GrowFromCenter(km_x), FadeIn(km_x_label), run_time=0.3)
        self.play(Create(km_dist_line), run_time=0.3)

        # === RIGHT SIDE: SAE ===
        sae_title = Text("SAE", font_size=22, color=BLUE)
        sae_title.shift(RIGHT * 3.5 + UP * 2.3)

        sae_bars = VGroup()
        bar_x_start = RIGHT * 2.2
        bar_width = 0.25
        bar_spacing = 0.35

        activations = [0.85, 0.0, 0.0, 0.0, 0.0]
        neuron_colors = [C1_COLOR, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY]

        for i, (val, col) in enumerate(zip(activations, neuron_colors)):
            if val > 0:
                bar = Rectangle(width=bar_width, height=val * 1.5, color=col, fill_opacity=0.8, stroke_width=1)
            else:
                bar = Rectangle(width=bar_width, height=0.08, color=TEXT_SECONDARY, fill_opacity=0.3, stroke_width=1)
            bar.move_to(bar_x_start + RIGHT * i * bar_spacing)
            bar.align_to(bar_x_start + DOWN * 0.8, DOWN)
            sae_bars.add(bar)

        z_label = MathTex("z", font_size=22, color=TEXT_PRIMARY)
        z_label.next_to(sae_bars, DOWN, buff=0.25)

        neuron_labels = VGroup()
        for i in range(3):
            nl = MathTex(f"z_{i+1}", font_size=14, color=neuron_colors[i])
            nl.next_to(sae_bars[i], UP, buff=0.1)
            neuron_labels.add(nl)

        self.play(FadeIn(sae_title, shift=DOWN * 0.1), run_time=0.3)
        self.play(*[GrowFromEdge(bar, DOWN) for bar in sae_bars], lag_ratio=0.05, run_time=0.5)
        self.play(FadeIn(z_label), *[FadeIn(nl) for nl in neuron_labels], run_time=0.3)

        # === HIGHLIGHTS AND CONNECTION ===
        active_highlight = SurroundingRectangle(sae_bars[0], color=POINT_COLOR, buff=0.05, stroke_width=2)
        centroid_highlight = Circle(radius=0.15, color=POINT_COLOR, stroke_width=2)
        centroid_highlight.move_to(km_centroids[0])

        self.play(Create(active_highlight), Create(centroid_highlight), run_time=0.4)

        connect_arrow = CurvedArrow(
            sae_bars[0].get_left() + LEFT * 0.1,
            km_centroids[0].get_right() + RIGHT * 0.2,
            color=POINT_COLOR, stroke_width=2, angle=-TAU/4, tip_length=0.15
        )
        self.play(Create(connect_arrow), run_time=0.5)

        same_label = Text("same selection", font_size=18, color=POINT_COLOR)
        same_label.next_to(connect_arrow, UP, buff=0.15)
        self.play(FadeIn(same_label, shift=DOWN * 0.1), run_time=0.3)

        # === EQUATIONS AT BOTTOM ===
        km_eq = MathTex(r"\arg\min_i \|x - c_i\|^2", font_size=22, color=BLUE)
        km_eq.shift(LEFT * 3.5 + DOWN * 2.5)

        sae_eq = MathTex(r"\arg\max_i \, z_i", font_size=22, color=BLUE)
        sae_eq.shift(RIGHT * 3.5 + DOWN * 2.5)

        equals = MathTex(r"=", font_size=32, color=POINT_COLOR)
        equals.move_to(DOWN * 2.5)

        self.play(Write(km_eq), Write(sae_eq), run_time=0.5)
        self.play(Write(equals), run_time=0.3)

        self.wait(1.5)


class MathScene(Scene):
    """Mathematical proof steps - for README section"""
    def construct(self):
        self.camera.background_color = BACKGROUND

        # Step 1: Distance decomposition
        step1_label = Text("1. expand the distance", font_size=20, color=TEXT_SECONDARY)
        step1_label.shift(UP * 2.5 + LEFT * 3)

        step1 = MathTex(
            r"\|x - c\|^2", r"=", r"\|x\|^2 - 2\langle x, c \rangle + \|c\|^2",
            font_size=26
        )
        step1[0].set_color(TEXT_PRIMARY)
        step1[2].set_color(TEXT_PRIMARY)
        step1.next_to(step1_label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(FadeIn(step1_label, shift=RIGHT * 0.1), run_time=0.3)
        self.play(Write(step1[0]), run_time=0.4)
        self.play(Write(step1[1:]), run_time=0.6)

        # Step 2: Normalized centroids
        step2_label = Text("2. if centroids are normalized", font_size=20, color=TEXT_SECONDARY)
        step2_label.shift(UP * 0.7 + LEFT * 3)

        step2a = MathTex(r"\|c_i\| = 1", font_size=26, color=BLUE)
        step2a.next_to(step2_label, DOWN, buff=0.3, aligned_edge=LEFT)

        step2b = MathTex(
            r"\Rightarrow \arg\min_i \|x - c_i\|^2 = \arg\max_i \langle x, c_i \rangle",
            font_size=24, color=TEXT_PRIMARY
        )
        step2b.next_to(step2a, DOWN, buff=0.25, aligned_edge=LEFT)

        self.play(FadeIn(step2_label, shift=RIGHT * 0.1), run_time=0.3)
        self.play(Write(step2a), run_time=0.4)
        self.play(Write(step2b), run_time=0.6)

        # Step 3: ReLU preserves argmax
        step3_label = Text("3. ReLU preserves ordering", font_size=20, color=TEXT_SECONDARY)
        step3_label.shift(DOWN * 1.2 + LEFT * 3)

        step3 = MathTex(
            r"a > b, \, a > 0 \;\Rightarrow\; \text{ReLU}(a) > \text{ReLU}(b)",
            font_size=24, color=TEXT_PRIMARY
        )
        step3.next_to(step3_label, DOWN, buff=0.3, aligned_edge=LEFT)

        # ReLU image on the right
        relu_img = ImageMobject("/home/qtzx/Codebase/sae-kmeans/assets/relu.png")
        relu_img.scale(0.7)
        relu_img.shift(RIGHT * 4 + DOWN * 0.3)

        self.play(FadeIn(step3_label, shift=RIGHT * 0.1), run_time=0.3)
        self.play(Write(step3), FadeIn(relu_img, shift=LEFT * 0.2), run_time=0.6)

        # QED
        qed = MathTex(r"\therefore \quad \text{SAE top-1} = \text{k-means}", font_size=28, color=BLUE)
        qed.shift(DOWN * 2.8)
        qed_box = SurroundingRectangle(qed, color=BLUE, buff=0.2, stroke_width=2)

        self.play(Write(qed), run_time=0.6)
        self.play(Create(qed_box), run_time=0.4)
        self.wait(1.5)
