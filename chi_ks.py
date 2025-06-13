import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import chi2
import random

# Kolmogorov-Smirnov Test for Uniform Distribution
def ks_test(data, level_of_significance):
    d, p_value = stats.kstest(data, 'uniform', args=(min(data), max(data) - min(data))) # Adjusted for range
    if p_value <= level_of_significance:
        ks_result = 'Reject H0 (Dependent)'
    else:
        ks_result = 'Accept H0 (Independent)'
    return d, p_value, ks_result

# Chi-Square Test for Uniform Distribution
def chi_square_test(numbers, num_intervals, level_of_significance):
    """Performs a Chi-square test for uniformity on a list of numbers."""
    min_val = min(numbers)
    max_val = max(numbers)
    interval_size = (max_val - min_val) / num_intervals

    observed_frequencies = [0] * num_intervals
    for num in numbers:
        interval_index = min(num_intervals - 1, int((num - min_val) / interval_size))
        observed_frequencies[interval_index] += 1

    expected_frequency = len(numbers) / num_intervals
    chi_square_statistic = 0
    for observed in observed_frequencies:
        chi_square_statistic += (observed - expected_frequency) ** 2 / expected_frequency

    degrees_of_freedom = num_intervals - 1
    p_value = 1 - chi2.cdf(chi_square_statistic, degrees_of_freedom)

    if p_value <= level_of_significance:
        chi_result = 'Reject H0 (Dependent)'
    else:
        chi_result = 'Accept H0 (Independent)'

    return chi_square_statistic, degrees_of_freedom, p_value, chi_result

# Plotting the Histogram
def plot_histogram(data, bins=10):
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title('Histogram of Input Random Numbers')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()

# Function to Generate Random Numbers
def generate_random_numbers(quantity, min_value, max_value, precision, level_of_significance):
    """Generates random numbers and performs the Chi-square and K-S tests."""
    random_numbers = []
    for _ in range(quantity):
        random_number = round(random.uniform(min_value, max_value), precision)
        random_numbers.append(random_number)

    print("\nGenerated Random Numbers:")
    for i, num in enumerate(random_numbers):
        print(f"{num:.{precision}f}", end=" ")
        if (i + 1) % 10 == 0:
            print()  # new line after 10 numbers

    # Perform Chi-square test
    chi_square, degrees_freedom, p_value, chi_result = chi_square_test(random_numbers, 10, level_of_significance)  # 10 intervals

    # Perform K-S test
    d, ks_p_value, ks_result = ks_test(random_numbers, level_of_significance)

    # Display results in the requested format
    print("\n" + "-"*85)
    print(f"{'Chi-square Test:':<40}| {'K-S Test:'}")
    print("-"*85)
    print(f"statistic: {chi_square:.4f},{' ' * 25}| D-statistic = {d:.4f}")
    print(f"Degrees of freedom: {degrees_freedom},{' ' * 7}| P-value = {ks_p_value:.4f}")
    print(f"P-value: {p_value:.4f},{' ' * 13}|")
    print(f"{chi_result:<40}| {ks_result}")
    print("-"*85)

    print("\nExplanation:")
    print(f"- Chi-Square Test: {chi_result}. The p-value of {p_value:.4f} is {'less than' if p_value <= level_of_significance else 'greater than'} the level of significance of {level_of_significance}.")
    print(f"- K-S Test: {ks_result}. The p-value of {ks_p_value:.4f} is {'less than' if ks_p_value <= level_of_significance else 'greater than'} the level of significance of {level_of_significance}.")

    return random_numbers

# Main function
def main():
    # User details
    name = "Rojesh Humagain"
    roll_number = "16"

    print(f"Name: {name}")
    print(f"Roll Number: {roll_number}")

    # Get user inputs
    quantity = int(input("Enter the number of random numbers to generate: "))
    min_value = float(input("Enter the minimum value [0.0]: ") or "0.0")
    max_value = float(input("Enter the maximum value [1.0]: ") or "1.0")
    precision = int(input("Enter decimal precision [5]: ") or "0")
    level_of_significance = float(input("Enter level of significance: "))

    if min_value >= max_value:
        print("Error: Invalid input - Minimum value must be less than maximum value.")
    else:
        # Generate random numbers and perform tests
        generated_numbers = generate_random_numbers(quantity, min_value, max_value, precision, level_of_significance)

        # Plot histogram
        plot_histogram(generated_numbers)

if __name__ == "__main__":
    main()