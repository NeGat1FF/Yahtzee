from main import roll, combos
from collections import Counter

# Parameters
number_of_bets = 1_000_000
bet = 10
desired_rtp = 0.95  # 95%

# Step 1: Simulate outcomes
combo_counter = Counter()
for _ in range(number_of_bets):
    combo, _ = roll()
    combo_counter[combo] += 1

# Step 2: Calculate real probabilities
probabilities = {k: v / number_of_bets for k, v in combo_counter.items()}

# Step 3: Calculate current RTP
current_rtp = sum(probabilities[k] * combos[k] for k in combos)

# Step 4: Scale payouts to get desired RTP
scaling_factor = desired_rtp / current_rtp
adjusted_combos = {k: round(v * scaling_factor, 2) for k, v in combos.items()}

# Step 5: Recalculate new RTP with adjusted payouts
new_rtp = sum(probabilities[k] * adjusted_combos[k] for k in adjusted_combos)

# Output
print("Observed Probabilities:")
for k in sorted(probabilities):
    print(f"{k}: {probabilities[k]:.6f}")

print("\nOriginal Payouts:")
for k in sorted(combos):
    print(f"{k}: {combos[k]}")

print(f"\nOriginal RTP: {current_rtp:.4f} ({current_rtp * 100:.2f}%)")
print(f"Scaling Factor: {scaling_factor:.4f}")

print("\nAdjusted Payouts:")
for k in sorted(adjusted_combos):
    print(f"{k}: {adjusted_combos[k]}")

print(f"\nAdjusted RTP: {new_rtp:.4f} ({new_rtp * 100:.2f}%)")
