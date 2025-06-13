import numpy as np
import os
from scipy.stats import chi2
from collections import Counter
from tabulate import tabulate

def generate_random_numbers(quantity, min_val=0.0, max_val=1.0, precision=5, filename="pokerrandom.txt"):
    numbers = np.round(np.random.uniform(min_val, max_val, quantity), precision)

    try:
        with open(filename, 'w') as file:
            for num in numbers:
                file.write(f"{num:.{precision}f}\n")

        # Display numbers in rows of 10
        print("\nGenerated Random Numbers:")
        for i in range(0, len(numbers), 10):
            print(" | ".join(map(str, numbers[i:i+10])))

        print(f"\nAll numbers are saved in '{filename}'.")

    except IOError:
        print(f"Error: Unable to write to file '{filename}'.")

    return numbers

def load_random_numbers(filename):
    numbers = []
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return numbers

    with open(filename, 'r') as file:
        numbers = [float(line.strip()) for line in file if line.strip().replace('.', '', 1).isdigit()]

    return numbers

def get_digit_pattern(number, precision):
    digits = str(number).replace('.', '')[:precision]
    return ''.join(sorted(digits))

def poker_test(numbers, alpha, precision):
    n = len(numbers)
    digit_patterns = [get_digit_pattern(num, precision) for num in numbers]
    counts = Counter(digit_patterns)

    unique_patterns = len(counts)
    expected = n / unique_patterns if unique_patterns else 1
    chi_square_stat = sum((count - expected) ** 2 / expected for count in counts.values())

    degrees_of_freedom = unique_patterns - 1
    p_value = 1 - chi2.cdf(chi_square_stat, df=degrees_of_freedom)

    return ("Accepted" if p_value > alpha else "Rejected"), chi_square_stat, p_value

def get_user_input():
    while True:
        try:
            quantity = int(input("Enter the number of random numbers to generate: "))
            if quantity > 0:
                break
            print("Quantity must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            min_val = float(input("Enter the minimum value [0.0]: ") or 0.0)
            max_val = float(input("Enter the maximum value [1.0]: ") or 1.0)
            if min_val < max_val:
                break
            print("Minimum value must be less than maximum value.")
        except ValueError:
            print("Invalid input. Please enter a float.")

    while True:
        try:
            precision = int(input("Enter decimal precision [5]: ") or 5)
            if 1 <= precision <= 10:
                break
            print("Precision must be between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            alpha = float(input("Enter the significance level (alpha): "))
            if 0 < alpha < 1:
                break
            print("Alpha must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a float.")

    return quantity, min_val, max_val, precision, alpha

if __name__ == "__main__":
    quantity, min_val, max_val, precision, alpha = get_user_input()

    generate_random_numbers(quantity, min_val, max_val, precision, "pokerrandom.txt")

    numbers = load_random_numbers("pokerrandom.txt")

    result, chi_square_stat, p_value = poker_test(numbers, alpha, precision)

    print("\nPoker Test Results:")
    table = [
        ["Parameter", "Value"],
        ["Chi-square Statistic", chi_square_stat],
        ["P-value", p_value],
        ["Result", result]
    ]
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

    if p_value == 0:
        print("P-value is 0.0, suggesting non-randomness. Increase precision for meaningful results.")
