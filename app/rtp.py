from main import roll, combos

number_of_bets = 1_000_000
bet = 10

total_winnings = 0
for i in range(number_of_bets):
    combo, _ = roll()
    total_winnings += bet * combos[combo]

print((total_winnings / (bet * number_of_bets)) * 100)
