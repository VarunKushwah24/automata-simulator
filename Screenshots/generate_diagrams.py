"""
Automata Theory Simulator - Diagram and Visual Asset Generator
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = os.path.abspath(os.path.dirname(__file__))

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, "CSET302 Automata Simulator: System Architecture & Workflow",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')
    ax.text(0.5, 0.90, "Topic 14: Mealy <-> Moore Bidirectional Conversion with Output Preservation",
            fontsize=11, style='italic', ha='center', color='#475569')

    # Boxes:
    # 1. Input Layer
    rect_in = patches.FancyBboxPatch((0.05, 0.55), 0.22, 0.25, boxstyle="round,pad=0.03",
                                    facecolor="#eff6ff", edgecolor="#2563eb", linewidth=2)
    ax.add_patch(rect_in)
    ax.text(0.16, 0.74, "1. Dynamic Input Layer", fontsize=11, fontweight='bold', ha='center', color='#1e3a8a')
    ax.text(0.16, 0.64, "• JSON Import / Export\n• Interactive Table GUI\n• Academic Presets (7)\n• 6-Tuple Definitions",
            fontsize=9, ha='center', color='#334155')

    # 2. Validation & Model Layer
    rect_val = patches.FancyBboxPatch((0.37, 0.55), 0.26, 0.25, boxstyle="round,pad=0.03",
                                     facecolor="#f5f3ff", edgecolor="#8b5cf6", linewidth=2)
    ax.add_patch(rect_val)
    ax.text(0.50, 0.74, "2. Validator & Core Engine", fontsize=11, fontweight='bold', ha='center', color='#5b21b6')
    ax.text(0.50, 0.64, "• AutomataValidator\n• Completeness & Determinism\n• MooreMachine (Q, Σ, Δ, δ, λ, q0)\n• MealyMachine (Q, Σ, Δ, δ, λ', q0)",
            fontsize=9, ha='center', color='#334155')

    # 3. Conversion Engine
    rect_conv = patches.FancyBboxPatch((0.73, 0.55), 0.22, 0.25, boxstyle="round,pad=0.03",
                                      facecolor="#ecfdf5", edgecolor="#10b981", linewidth=2)
    ax.add_patch(rect_conv)
    ax.text(0.84, 0.74, "3. Conversion Algorithms", fontsize=11, fontweight='bold', ha='center', color='#065f46')
    ax.text(0.84, 0.64, "• Moore -> Mealy Mapping\n• Mealy -> Moore State Splitting\n• Start Output Assignment\n• Dead State Pruning",
            fontsize=9, ha='center', color='#334155')

    # Arrows between top layer
    ax.annotate("", xy=(0.36, 0.67), xytext=(0.28, 0.67),
                arrowprops=dict(arrowstyle="->", lw=2.5, color="#2563eb"))
    ax.annotate("", xy=(0.72, 0.67), xytext=(0.64, 0.67),
                arrowprops=dict(arrowstyle="->", lw=2.5, color="#8b5cf6"))

    # Bottom Layer: Visualization & Verification
    # 4. Visualization & Simulator
    rect_vis = patches.FancyBboxPatch((0.10, 0.12), 0.35, 0.30, boxstyle="round,pad=0.03",
                                     facecolor="#fffbeb", edgecolor="#f59e0b", linewidth=2)
    ax.add_patch(rect_vis)
    ax.text(0.275, 0.36, "4. Visualization & Tape Simulator", fontsize=11, fontweight='bold', ha='center', color='#92400e')
    ax.text(0.275, 0.24, "• Interactive SVG Graph Diagrams\n• Dual Synchronized Tape Player\n• Active State & Transition Animation\n• Fast Playback & Step Controls",
            fontsize=9, ha='center', color='#334155')

    # 5. Verification & Testing Suite
    rect_ver = patches.FancyBboxPatch((0.55, 0.12), 0.35, 0.30, boxstyle="round,pad=0.03",
                                     facecolor="#fef2f2", edgecolor="#ef4444", linewidth=2)
    ax.add_patch(rect_ver)
    ax.text(0.725, 0.36, "5. Equivalence Verification Suite", fontsize=11, fontweight='bold', ha='center', color='#991b1b')
    ax.text(0.725, 0.24, "• Formal Theorem: Moore = λ(q0) · Mealy\n• Automated T01-T10 Test Runner\n• Boundary & Edge Case Checking\n• Milestone-II Rubric Compliance",
            fontsize=9, ha='center', color='#334155')

    # Connect top to bottom
    ax.annotate("", xy=(0.275, 0.43), xytext=(0.50, 0.54),
                arrowprops=dict(arrowstyle="->", lw=2.5, color="#475569", connectionstyle="arc3,rad=-0.15"))
    ax.annotate("", xy=(0.725, 0.43), xytext=(0.84, 0.54),
                arrowprops=dict(arrowstyle="->", lw=2.5, color="#475569", connectionstyle="arc3,rad=0.15"))

    plt.tight_layout()
    out_path = os.path.join(output_dir, "architecture_diagram.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def generate_state_splitting_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')

    ax.text(0.5, 0.92, "Mealy to Moore State Splitting Principle (Topic 14)",
            fontsize=14, fontweight='bold', ha='center', color='#0f172a')

    # Left: Mealy state with multiple incoming outputs
    ax.text(0.25, 0.80, "Mealy State q with Multiple Outputs", fontsize=11, fontweight='bold', ha='center', color='#2563eb')
    c_mealy = patches.Circle((0.25, 0.45), 0.12, facecolor="#eff6ff", edgecolor="#2563eb", linewidth=2.5)
    ax.add_patch(c_mealy)
    ax.text(0.25, 0.45, "q", fontsize=14, fontweight='bold', ha='center', va='center')

    # Incoming transitions
    ax.annotate("In '0', out '0'", xy=(0.17, 0.52), xytext=(0.04, 0.65),
                arrowprops=dict(arrowstyle="->", lw=2, color="#475569"), fontsize=9, fontweight='600')
    ax.annotate("In '1', out '1'", xy=(0.17, 0.38), xytext=(0.04, 0.25),
                arrowprops=dict(arrowstyle="->", lw=2, color="#475569"), fontsize=9, fontweight='600')

    # Arrow to split
    ax.annotate("State Splits!", xy=(0.52, 0.45), xytext=(0.40, 0.45),
                arrowprops=dict(arrowstyle="->", lw=3, color="#ef4444"), fontsize=11, fontweight='bold', color="#ef4444", va='center')

    # Right: Split Moore states
    ax.text(0.75, 0.80, "Resulting Moore States", fontsize=11, fontweight='bold', ha='center', color='#10b981')
    c_moore1 = patches.Circle((0.75, 0.62), 0.10, facecolor="#ecfdf5", edgecolor="#10b981", linewidth=2.5)
    c_moore2 = patches.Circle((0.75, 0.28), 0.10, facecolor="#ecfdf5", edgecolor="#10b981", linewidth=2.5)
    ax.add_patch(c_moore1)
    ax.add_patch(c_moore2)

    ax.text(0.75, 0.64, "q_0", fontsize=12, fontweight='bold', ha='center')
    ax.text(0.75, 0.58, "λ = 0", fontsize=10, color='#dc2626', fontweight='bold', ha='center')

    ax.text(0.75, 0.30, "q_1", fontsize=12, fontweight='bold', ha='center')
    ax.text(0.75, 0.24, "λ = 1", fontsize=10, color='#dc2626', fontweight='bold', ha='center')

    plt.tight_layout()
    out_path = os.path.join(output_dir, "state_splitting_principle.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_state_splitting_diagram()
