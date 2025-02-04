import pandas as pd
import os
import yaml

# Load configurations from config.yaml
config_file = 'C:/Users/user/Desktop/AI/ML Projects/DeepClean/src/cleanshelf/configuration/config.yaml'

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Extract the input file and output folder from config
input_file = config.get('input_file', 'C:/Users/user/Desktop/AI/ML Projects/DeepClean/Data/cleanshelf/Cosmetics december 2024 sales data.xlsx')
output_folder = config.get('output_folder', 'C:/Users/user/Desktop/AI/ML Projects/DeepClean/artifacts/cleanshelf/headers')

# Load the Excel file, skipping the first 8 rows and without changing column names
data = pd.read_excel(input_file, skiprows=8, header=None)

# Drop the first 3 columns
data.drop(columns=data.columns[:3], inplace=True)

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Save the cleaned data to an Excel file
output_file = os.path.join(output_folder, 'cleaned_data.xlsx')
data.to_excel(output_file, index=False, header=False)  # Set header=False to avoid adding a header row

print(f"File saved as {output_file}")
