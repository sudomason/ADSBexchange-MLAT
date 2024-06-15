import pandas as pd
import gzip
import json
import os
import glob
from datetime import datetime
import csv
from collections import defaultdict

# Directory containing the files - CHANGE TO SUIT YOUR FILE LOCATION 
directory_path = '/Users/jonathonmason/Downloads/ADSBExchange_files/'
output_directory = '/Users/jonathonmason/Documents/Python Learning/ADSBExchange data/mel'

# Create a new folder within output_directory with today's date
today_date = datetime.now().strftime('%Y-%m-%d')
output_folder = os.path.join(output_directory, f'DublinADSB_output_{today_date}')
os.makedirs(output_folder, exist_ok=True)

# Combined output file within the new folder
combined_output_file = os.path.join(output_folder, f'combined_filtered_data.csv')

# Define the geographic boundaries for DALAS and altitude range
latitude_min, latitude_max = 53.0, 54.0
longitude_min, longitude_max = -7.0, -5.0
altitude_min, altitude_max = 0, 5000  # Example altitude range, modify as needed

def is_gzipped(file_path):
    """ Check if the file is gzipped """
    with open(file_path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'

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

# List to store all filtered dataframes
all_filtered_dataframes = []

# Process each .json.gz file in the directory
for file_path in glob.glob(os.path.join(directory_path, '*.json.gz')):
    try:
        if is_gzipped(file_path):
            # Open and read the gzip file
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # Open and read the regular JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        # Extract the aircraft data
        aircraft_data = data.get('aircraft', [])

        # Convert the aircraft data to a pandas DataFrame
        df = pd.DataFrame(aircraft_data)

        # Convert 'alt_baro' column to numeric type
        df['alt_baro'] = pd.to_numeric(df['alt_baro'], errors='coerce')  # coerce invalid parsing to NaN

        # Filter the data
        filtered_data = df[
            (df['lat'] >= latitude_min) & (df['lat'] <= latitude_max) &
            (df['lon'] >= longitude_min) & (df['lon'] <= longitude_max) &
            (df['alt_baro'].between(altitude_min, altitude_max, inclusive='both'))  # specify inclusive='both'
        ]

        # Append filtered dataframe to the list
        all_filtered_dataframes.append(filtered_data)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred processing {file_path}: {str(e)}")

# Combine all filtered dataframes into a single dataframe
combined_df = pd.concat(all_filtered_dataframes, ignore_index=True)

# Save the combined filtered data to a new CSV file within the output folder
combined_df.to_csv(combined_output_file, index=False)
print(f"Combined filtered data saved to {combined_output_file}")

# Count entries in the CSV file
column_name = 'type'  # Replace with the column name you want to filter/count
entry_counts, total_entries = count_entries(combined_output_file, column_name)
