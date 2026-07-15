import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# ---------------------------------------
# Read CRP File
# ---------------------------------------

filename = "CRP_Output.txt"

challenge = []
lfsr = []
response = []

with open(filename, "r") as file:

    for line in file:

        parts = line.strip().split()

        if len(parts) != 3:
            continue

        challenge.append(parts[0])
        lfsr.append(parts[1])
        response.append(parts[2])

# ---------------------------------------
# Convert to DataFrame
# ---------------------------------------

df = pd.DataFrame({

    "Challenge": challenge,
    "LFSR": lfsr,
    "Response": response

})

# ---------------------------------------
# Basic Statistics
# ---------------------------------------

total = len(df)

zeros = (df["Response"] == "0").sum()
ones = (df["Response"] == "1").sum()

uniformity = (ones / total) * 100

print("\n==============================")
print("      CRP ANALYSIS")
print("==============================")

print("Total CRPs      :", total)
print("Response 0      :", zeros)
print("Response 1      :", ones)
print("Uniformity (%)  :", round(uniformity,2))

# ---------------------------------------
# Response Distribution
# ---------------------------------------

plt.figure(figsize=(6,4))

plt.bar(["0","1"], [zeros,ones])

plt.title("Response Distribution")

plt.xlabel("Response")

plt.ylabel("Count")

plt.savefig("response_distribution.png")

# ---------------------------------------
# LFSR Distribution
# ---------------------------------------

lfsr_counter = Counter(lfsr)

states = sorted(lfsr_counter.keys())

counts = [lfsr_counter[x] for x in states]

plt.figure(figsize=(8,4))

plt.bar(states,counts)

plt.title("Obfuscated Challenge Distribution")

plt.xlabel("4-bit LFSR Output")

plt.ylabel("Occurrences")

plt.savefig("lfsr_distribution.png")

# ---------------------------------------
# Response vs LFSR
# ---------------------------------------

table = pd.crosstab(df["LFSR"],df["Response"])

table.to_csv("response_vs_lfsr.csv")

print("\nLFSR Statistics\n")

print(table)

# ---------------------------------------
# Save Summary
# ---------------------------------------

with open("summary.txt","w") as f:

    f.write("CRP ANALYSIS\n\n")

    f.write(f"Total CRPs : {total}\n")

    f.write(f"Response 0 : {zeros}\n")

    f.write(f"Response 1 : {ones}\n")

    f.write(f"Uniformity : {uniformity:.2f}%\n")

print("\nFiles Generated Successfully!")

print("response_distribution.png")

print("lfsr_distribution.png")

print("response_vs_lfsr.csv")

print("summary.txt")