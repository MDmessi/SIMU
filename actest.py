import numpy as np
from scipy.special import erfinv
from tabulate import tabulate
import os

print("Name: Rojesh Humagain")
print("Roll No: 16")

def generate_random_numbers(quantity, min_val=0.0, max_val=1.0, precision=5, filename="acrandom.txt"):
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
    """Loads random numbers from a file, handling various formats and errors."""
    numbers = []
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return numbers  

    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    numbers.append(float(line.strip()))
                    if len(numbers) >= quantity:
                        break
                except ValueError:
                    print(f"Warning: Skipping invalid data in file '{filename}'.")
    except IOError:
        print(f"Error: Unable to read file '{filename}'.")

    return numbers

def autocorrelation_test(numbers, lag, alpha):
    """Performs the autocorrelation test and returns results."""
    n = len(numbers)
    if lag >= n:
        return "Invalid Lag", 0, 0, 0  

    mean = np.mean(numbers)
    numerator = sum((numbers[i] - mean) * (numbers[i + lag] - mean) for i in range(n - lag))
    denominator = sum((numbers[i] - mean) ** 2 for i in range(n))

    rho = numerator / denominator if denominator != 0 else 0  
    Z0 = rho * np.sqrt(n - lag)  

    try:
        Z_alpha = np.sqrt(2) * erfinv(1 - alpha)
    except ValueError:
        Z_alpha = float("inf")  

    result = "Accepted" if abs(Z0) < Z_alpha else "Rejected"
    return result, rho, Z0, Z_alpha

def get_user_input():
    """Gets user input with error handling and default values."""
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
            lag = int(input("Enter the lag (k): "))
            if 0 < lag < quantity:
                break
            print(f"Lag must be a positive integer less than {quantity}.")
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

    return quantity, min_val, max_val, precision, lag, alpha

if __name__ == "__main__":
    quantity, min_val, max_val, precision, lag, alpha = get_user_input()
    filename = "acrandom.txt"

    numbers = generate_random_numbers(quantity, min_val, max_val, precision, filename)
    numbers = load_random_numbers(filename, quantity)

    if len(numbers) < quantity:
        print("Autocorrelation test cannot be performed due to insufficient data.")
    else:
        result, rho, Z0, Z_alpha = autocorrelation_test(numbers, lag, alpha)

        table = [
            ["Parameter", "Value"],
            ["Mean", np.mean(numbers)],
            ["Rho (Autocorrelation Coefficient)", rho],
            ["Z0 (Test Statistic)", Z0],
            ["Z_alpha (Critical Value)", Z_alpha],
            ["Result", result]
        ]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
