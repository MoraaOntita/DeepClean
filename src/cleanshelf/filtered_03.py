import os
import pandas as pd

# Load the dataset
file_path = 'artifacts/cleanshelf/formatted/cleaned_data.csv'
data = pd.read_csv(file_path)

# Filter the data for suppliers from ALKHEMY BRANDS LIMITED
filtered_data = data[data['Supp_Name'] == 'ALKHEMY BRANDS LIMITED']

# Define output path
output_path = 'artifacts/cleanshelf/filtered/filtered_data.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the filtered data
filtered_data.to_csv(output_path, index=False)

print(f"Filtered data saved to: {output_path}")
