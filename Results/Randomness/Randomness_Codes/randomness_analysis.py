import math
import sys

# ===================================================
# Save Output to File + Terminal
# ===================================================

output_file = open("Randomness_Output.txt", "w", encoding="utf-8")

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            try:
                f.flush()
            except ValueError:
                pass

sys.stdout = Tee(sys.__stdout__, output_file)

# ===================================================
# Read CRP File
# ===================================================

filename = "CRP_Output.txt"

responses = []

with open(filename, "r") as f:

    for line in f:

        parts = line.strip().split()

        if len(parts) != 3:
            continue

        responses.append(parts[2])

responses = "".join(responses)

n = len(responses)

print("=" * 50)
print(" RANDOMNESS ANALYSIS")
print("=" * 50)

print("Total Response Bits :", n)

zeros = responses.count('0')
ones = responses.count('1')

print("Zeros :", zeros)
print("Ones  :", ones)

bias = abs(ones - zeros) / n

print("Bias :", round(bias, 6))

# ===================================================
# Shannon Entropy
# ===================================================

p0 = zeros / n
p1 = ones / n

entropy = 0

if p0 > 0:
    entropy -= p0 * math.log2(p0)

if p1 > 0:
    entropy -= p1 * math.log2(p1)

print("\nShannon Entropy :", round(entropy, 6), "bits")

# ===================================================
# Min Entropy
# ===================================================

pmax = max(p0, p1)

min_entropy = -math.log2(pmax)

print("Min Entropy :", round(min_entropy, 6), "bits")

# ===================================================
# Runs Test
# ===================================================

runs = 1

for i in range(1, n):

    if responses[i] != responses[i - 1]:
        runs += 1

print("\nNumber of Runs :", runs)

expected_runs = ((2 * zeros * ones) / n) + 1

print("Expected Runs :", round(expected_runs, 2))

# ===================================================
# Longest Run
# ===================================================

current = 1
maximum = 1

for i in range(1, n):

    if responses[i] == responses[i - 1]:

        current += 1

        if current > maximum:
            maximum = current

    else:

        current = 1

print("Longest Run :", maximum)

# ===================================================
# Transition Probability
# ===================================================

transition = 0

for i in range(1, n):

    if responses[i] != responses[i - 1]:
        transition += 1

transition_probability = transition / (n - 1)

print("\nTransition Probability :", round(transition_probability, 6))

# ===================================================
# Adjacent Bit Correlation
# ===================================================

same = 0

for i in range(n - 1):

    if responses[i] == responses[i + 1]:
        same += 1

auto = same / (n - 1)

print("Adjacent Bit Correlation :", round(auto, 6))

# ===================================================
# Overall Assessment
# ===================================================

print("\nOverall Assessment")

if entropy > 0.98 and bias < 0.05:
    print("PASS : Good Randomness")
else:
    print("WARNING : Randomness can be improved")

print("\nResults saved to Randomness_Output.txt")

# ===================================================
# Restore stdout and Close File
# ===================================================

sys.stdout = sys.__stdout__

output_file.close()