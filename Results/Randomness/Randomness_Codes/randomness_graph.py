import matplotlib.pyplot as plt

metrics = [
    "Entropy",
    "Min Entropy",
    "Transition\nProbability"
]

values = [
    0.99674,
    0.90617,
    0.46635
]

plt.figure(figsize=(8,5))

bars = plt.bar(
    metrics,
    values
)

plt.ylim(0,1.1)

plt.ylabel("Value")

plt.title(
    "Randomness Evaluation of Generated Responses",
    fontsize=14,
    fontweight="bold"
)

plt.grid(axis='y', linestyle='--', alpha=0.4)

for b in bars:

    h = b.get_height()

    plt.text(
        b.get_x()+b.get_width()/2,
        h+0.02,
        f"{h:.3f}",
        ha='center',
        fontweight='bold'
    )

plt.tight_layout()

plt.savefig(
    "Randomness_Evaluation.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("Saved : Randomness_Evaluation.png")