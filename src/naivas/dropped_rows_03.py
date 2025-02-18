import pandas as pd
import os

# Define file paths
input_file = r'artifacts\naivas\edited_columns\cleaned_data_transformed.csv'
output_folder = r'artifacts\naivas\edited_rows'
output_file = os.path.join(output_folder, 'cleaned_data_transformed.csv')

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the dataset
df = pd.read_csv(input_file)

# Drop rows where ITEMLOOKUPCODE contains 'Total'
df = df[df['ITEMLOOKUPCODE'] != 'Total']

# Save the cleaned dataset
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
