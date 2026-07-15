import matplotlib.pyplot as plt
import numpy as np

models = [
    "Logistic\nRegression",
    "Support\nVector\nMachine",
    "Random\nForest"
]

paper = [53.0, 53.0, 0]

yours = [54.95, 53.75, 53.60]

x = np.arange(len(models))

width = 0.35

plt.figure(figsize=(9,6))

bars1 = plt.bar(
    x-width/2,
    paper,
    width,
    label="Paper",
    color="#4E79A7"
)

bars2 = plt.bar(
    x+width/2,
    yours,
    width,
    label="Proposed FPGA"
)

plt.title(
    "Comparison with Published Work",
    fontsize=15,
    fontweight='bold'
)

plt.ylabel("Prediction Accuracy (%)")

plt.ylim(0,70)

plt.xticks(x, models)

plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.legend()

for b in bars1:
    h = b.get_height()
    if h != 0:
        plt.text(
            b.get_x()+b.get_width()/2,
            h+0.5,
            f"{h:.1f}",
            ha='center',
            fontsize=10,
            fontweight='bold'
        )

for b in bars2:
    h = b.get_height()
    plt.text(
        b.get_x()+b.get_width()/2,
        h+0.5,
        f"{h:.2f}",
        ha='center',
        fontsize=10,
        fontweight='bold'
    )

plt.tight_layout()

plt.savefig(
    "Paper_Comparison.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("Saved : Paper_Comparison.png")