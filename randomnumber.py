import random
from datetime import datetime

def generate_random_numbers():
    try:
        quantity = int(input("Enter the number of random numbers to generate: "))
        if quantity <= 0:
            print("Error: Invalid input - Quantity must be a positive integer.")
            return

        min_value = float(input("Enter the minimum value [0.0]: ") or "0.0")
        max_value = float(input("Enter the maximum value [1.0]: ") or "1.0")
        precision = int(input("Enter decimal precision [5]: ") or "5")

        if precision < 0:
            print("Error: Invalid input - Precision must be a non-negative integer.")
            return

        if min_value >= max_value:
            print("Error: Invalid input - Minimum value must be less than maximum value.")
            return

        filename = "randomnumber.txt"  # Fixed filename

        # Generate random numbers and store them in a list
        random_numbers = []
        for _ in range(quantity):
            random_number = round(random.uniform(min_value, max_value), precision)
            random_numbers.append(random_number)

        # Save numbers to the file in table form
        save_to_file_table(random_numbers, filename, per_row=10)

        print(f"\n random numbers are save in {filename} files","\n")

        show_stats = input("Would you like to see statistics? (yes/no): ").lower().startswith('y')

        if show_stats:
            min_val = min(random_numbers)
            max_val = max(random_numbers)
            avg_val = sum(random_numbers) / len(random_numbers)

            print("\nStatistics:")
            print(f"  Minimum value: {min_val}")
            print(f"  Maximum value: {max_val}")
            print(f"  Average value: {avg_val:.{precision}f} \n")

    except ValueError as e:
        print(f"Error: Invalid input - {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def save_to_file_table(numbers, filename, per_row=10):
    """Saves the numbers to a file in table form."""
    try:
        with open(filename, 'w') as file:
            # Determine the width of each column
            max_length = max(len(str(num)) for num in numbers)
            column_width = max_length + 4  # Add padding

            # Write the numbers in table format
            for i in range(0, len(numbers), per_row):
                row = ""
                for num in numbers[i:i + per_row]:
                    row += f"{str(num).ljust(column_width)}"
                file.write(row.rstrip() + "\n")

        
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    generate_random_numbers()