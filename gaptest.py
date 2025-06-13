import numpy as np
from scipy.stats import chi2
from tabulate import tabulate
import os

def generate_random_numbers(quantity, min_val=0.0, max_val=1.0, precision=5, filename="gaprandom.txt"):
    """Generates random numbers and saves them to a file."""
    numbers = np.round(np.random.uniform(min_val, max_val, quantity), precision)

    try:
        with open(filename, 'w') as file:
            for num in numbers:
                file.write(f"{num:.{precision}f}\n")

        print("\nGenerated Random Numbers:")
        for i in range(0, len(numbers), 10):
            print(" | ".join(map(str, numbers[i:i+10])))

        print(f"\nAll numbers are saved in '{filename}'.")

    except IOError:
        print(f"Error: Unable to write to file '{filename}'.")

    return numbers

def load_random_numbers(filename, quantity):
    numbers = []
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return numbers

    with open(filename, 'r') as file:
        while len(numbers) < quantity:
            line = file.readline().strip()
            if not line:
                break
            try:
                numbers.append(float(line))
            except ValueError:
                print(f"Skipping invalid line: {line}")

    return numbers

def gap_test(numbers, alpha, low, high):
    """Performs the gap test and returns the result."""
    gaps = []
    gap = 0
    in_range = False

    for number in numbers:
        if low <= number <= high:
            if in_range:
                gaps.append(gap)
                gap = 0
            in_range = True
        else:
            if in_range:
                gap += 1

    if not gaps:
        return "Not enough gaps", 0, 0, 0, 1  # Avoid division by zero

    k = len(gaps)
    mean_gap = np.mean(gaps) if gaps else 0
    expected = k  # The expected number of gaps is k
    observed = np.sum(gaps)

    chi_square_stat = (observed - expected) ** 2 / expected if expected != 0 else 0
    df = max(k - 1, 1)  # Ensure degrees of freedom is at least 1
    p_value = 1 - chi2.cdf(chi_square_stat, df=df)

    return ("Accepted" if p_value > alpha else "Rejected"), k, mean_gap, chi_square_stat, p_value

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
            low = float(input("Enter the lower bound: "))
            high = float(input("Enter the upper bound: "))
            if low < high:
                break
            print("Lower bound must be less than upper bound.")
        except ValueError:
            print("Invalid input. Please enter a float.")

    while True:
        try:
            alpha = float(input("Enter the significance level (alpha): "))
            if 0 < alpha < 1:
                break
            print("Alpha must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a float.")

    return quantity, min_val, max_val, precision, low, high, alpha

if __name__ == "__main__":
    quantity, min_val, max_val, precision, low, high, alpha = get_user_input()
    numbers = generate_random_numbers(quantity, min_val, max_val, precision, "gaprandom.txt")
    numbers = load_random_numbers("gaprandom.txt", quantity)

    if len(numbers) < quantity:
        print("Not enough data to perform the test.")
    else:
        result, k, mean_gap, chi_square_stat, p_value = gap_test(numbers, alpha, low, high)

        table = [
            ["Parameter", "Value"],
            ["Number of Gaps", k],
            ["Mean Gap", mean_gap],
            ["Chi-square Statistic", chi_square_stat],
            ["P-value", p_value],
            ["Result", result]
        ]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
