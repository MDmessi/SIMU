import numpy as np
from scipy.stats import chisquare
from tabulate import tabulate
import os

def generate_random_numbers(seed, num_digits, quantity):
    """Generate random numbers using the mid-square method."""
    random_numbers = []
    for _ in range(quantity):
        # Square the seed
        squared = seed ** 2
        # Zero pad the squared number to make sure it has at least 2 * num_digits
        squared_str = str(squared).zfill(num_digits * 2)
        # Extract the middle digits based on num_digits
        mid_start = (len(squared_str) - num_digits) // 2
        mid_end = mid_start + num_digits
        # Extract middle digits and update seed
        seed = int(squared_str[mid_start:mid_end])
        random_numbers.append(seed)
    return random_numbers

def chi_square_test(numbers, num_bins=10, alpha=0.05):
    """Performs Chi-Square test to check if numbers are uniformly distributed."""
    # Create bins and count the occurrences of numbers in each bin
    counts, bin_edges = np.histogram(numbers, bins=num_bins, range=(0, 9999))
    
    # Expected frequencies if the numbers were uniformly distributed
    expected = np.full_like(counts, fill_value=len(numbers) / num_bins)
    
    # Perform the Chi-square test
    chi2_stat, p_value = chisquare(counts, expected)
    
    # Determine acceptance based on the p-value
    result = "Accepted" if p_value > alpha else "Rejected"
    return result, chi2_stat, p_value

def save_numbers_to_file(numbers, filename="midsquare.txt"):
    """Saves the generated random numbers to a file."""
    with open(filename, 'w') as file:
        for num in numbers:
            file.write(f"{num}\n")
    print(f"Random numbers saved to {filename}")

def get_user_input():
    """Prompts the user for input and returns the values."""
    while True:
        try:
            seed = int(input("Enter the seed (number of digits must match): "))
            num_digits = int(input("Enter the number of digits to consider: "))
            quantity = int(input("Enter the number of random numbers to generate: "))
            alpha = float(input("Enter the significance level (alpha): "))
            if 0 < alpha < 1:
                break
            else:
                print("Alpha must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter valid integers or floats.")
    return seed, num_digits, quantity, alpha

def display_numbers_in_rows(numbers, numbers_per_row=10):
    """Displays the numbers in rows with 10 numbers per row."""
    for i in range(0, len(numbers), numbers_per_row):
        print(" | ".join(str(num) for num in numbers[i:i+numbers_per_row]))

if __name__ == "__main__":
    # Get user input
    seed, num_digits, quantity, alpha = get_user_input()

    # Generate random numbers using Mid-Square method
    random_numbers = generate_random_numbers(seed, num_digits, quantity)

    # Save the numbers to a file
    save_numbers_to_file(random_numbers)

    # Display the numbers in rows of 10 numbers each
    print("\nGenerated Random Numbers:")
    display_numbers_in_rows(random_numbers)

    # Test randomness using Chi-Square test
    result, chi2_stat, p_value = chi_square_test(random_numbers)

    # Display results
    table = [
        ["Parameter", "Value"],
        ["Chi-square Statistic", chi2_stat],
        ["P-value", p_value],
        ["Result", result]
    ]
    print("\nChi-Square Test Results:")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
