import csv
from collections import defaultdict

def count_entries(csv_file, column_name):
    # Dictionary to store counts of each entry
    entry_counts = defaultdict(int)
    total_entries = 0  # To keep track of total entries

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if column_name in row:
                entry = row[column_name].strip()  # Ensure no leading/trailing whitespace affects counting
                entry_counts[entry] += 1
                total_entries += 1

    # Print the counts and percentages
    print(f"Counts of entries under '{column_name}':")
    for entry, count in entry_counts.items():
        percentage = (count / total_entries) * 100 if total_entries > 0 else 0
        print(f"{entry}: {count} ({percentage:.2f}%)")

    # Print total items in the column
    print(f"Total items in '{column_name}': {total_entries}")

    return entry_counts, total_entries

# Example usage:
if __name__ == "__main__":
    csv_file = '/Users/jonathonmason/Documents/Python Learning/ADSBExchange data/ADSB_output_2024-06-15/combined_filtered_data.csv'  # Replace with your CSV file path
    column_name = 'type'  # Replace with the column name you want to filter/count

    entry_counts, total_entries = count_entries(csv_file, column_name)
