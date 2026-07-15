import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# ==========================================================
# READ CRP FILE
# ==========================================================

filename = "CRP_Output.txt"

X_challenge = []
X_full = []
y = []

with open(filename, "r") as f:

    for line in f:

        data = line.strip().split()

        if len(data) != 3:
            continue

        challenge = data[0]
        lfsr = data[1]
        response = int(data[2])

        # Paper assumption
        X_challenge.append([int(b) for b in challenge])

        # Internal analysis
        X_full.append([int(b) for b in (challenge + lfsr)])

        y.append(response)

print("="*70)
print("        LFSR-APUF MODELING ATTACK")
print("="*70)

print("\nTotal CRPs :", len(y))

# ==========================================================
# MODELS
# ==========================================================

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Support Vector Machine":
        SVC(kernel="rbf"),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

}

# ==========================================================
# FUNCTION
# ==========================================================

def evaluate(feature_set, title):

    print("\n")
    print("="*70)
    print(title)
    print("="*70)

    X_train, X_test, y_train, y_test = train_test_split(
        feature_set,
        y,
        test_size=0.20,
        random_state=42
    )

    results = []

    for name, model in models.items():

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        acc = accuracy_score(y_test, pred) * 100

        print(f"{name:25s}: {acc:.2f}%")

        results.append(acc)

    return results

# ==========================================================
# EXPERIMENT 1
# ==========================================================

paper_results = evaluate(
    X_challenge,
    "EXPERIMENT 1 : PAPER ASSUMPTION (Challenge Only)"
)

# ==========================================================
# EXPERIMENT 2
# ==========================================================

full_results = evaluate(
    X_full,
    "EXPERIMENT 2 : Challenge + LFSR Output"
)

# ==========================================================
# TABLE
# ==========================================================

df = pd.DataFrame({

    "Model":[
        "Logistic Regression",
        "Support Vector Machine",
        "Random Forest"
    ],

    "Challenge Only (%)":paper_results,

    "Challenge + LFSR (%)":full_results

})

print("\n")
print("="*70)
print(df)
print("="*70)

df.to_csv("ML_Comparison.csv", index=False)

# ==========================================================
# GRAPH
# ==========================================================

plt.figure(figsize=(10,6))

x = range(len(df))

bars1 = plt.bar(
    [i-0.2 for i in x],
    df["Challenge Only (%)"],
    width=0.4,
    label="Challenge Only",
    color="#4E79A7"
)

bars2 = plt.bar(
    [i+0.2 for i in x],
    df["Challenge + LFSR (%)"],
    width=0.4,
    label="Challenge + LFSR",
    color="#F28E2B"
)

plt.xticks(
    x,
    df["Model"],
    fontsize=11
)

plt.ylabel(
    "Prediction Accuracy (%)",
    fontsize=12
)

plt.xlabel(
    "Machine Learning Models",
    fontsize=12
)

plt.title(
    "Prediction Accuracy under Modeling Attack",
    fontsize=14,
    fontweight='bold'
)

plt.ylim(0,70)

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.4
)

plt.legend()

# -------------------------------------------------
# Write values above each bar
# -------------------------------------------------

for bar in bars1:

    height = bar.get_height()

    plt.text(
        bar.get_x()+bar.get_width()/2,
        height+0.6,
        f"{height:.2f}",
        ha='center',
        fontsize=10,
        fontweight='bold'
    )

for bar in bars2:

    height = bar.get_height()

    plt.text(
        bar.get_x()+bar.get_width()/2,
        height+0.6,
        f"{height:.2f}",
        ha='center',
        fontsize=10,
        fontweight='bold'
    )

plt.tight_layout()

plt.savefig(
    "ML_Comparison.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("\nSaved : ML_Comparison.csv")
print("Saved : ML_Comparison.png")