from decimal import Decimal, getcontext
from math import factorial

def calculate_pi(precision):
    getcontext().prec = precision
    C = 426880 * Decimal(10005).sqrt()
    L = 13591409
    X = 1
    M = 1
    K = 6
    S = L
    for i in range(1, precision):
        M = M * (K ** 3 - 16 * K) // (i ** 3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    pi = C / S
    return pi

# Set the desired precision (number of decimal places)
precision = 1000

# Calculate Pi
pi = calculate_pi(precision + 1)  # Add 1 to account for the integer part

# Format and print the result
pi_str = f"{pi:.{precision}f}"
print(f"Pi to {precision} decimal places:")
print(pi_str)

# Optionally, you can write the result to a file
with open('pi_1000_digits.txt', 'w') as f:
    f.write(pi_str)