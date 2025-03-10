import os
import pandas as pd

# Define file paths
input_file_path = "Data/naivas/Naivas Monthly Sales Report - 2025-03-04T142408.629.xlsx"
output_folder_path = "artifacts/naivas/formatted"

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Load the Excel file with multi-level headers
df = pd.read_excel(input_file_path, header=[0, 1])  # Read first two rows as headers

# Inspect the first few rows before cleaning column names
print("Before cleaning column names:")
print(df.head())

# Flatten multi-level columns by joining them with an underscore
df.columns = [
    "_".join([str(col[0]), str(col[1])]) if isinstance(col, tuple) else col 
    for col in df.columns
]

df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

# Rename specific columns
df.rename(columns={
    'Unnamed: 0_level_0_ITEMLOOKUPCODE': 'ITEMLOOKUPCODE',
    'Unnamed: 2_level_0_BARCODE': 'BARCODE',
    'Unnamed: 5_level_0_DESCRIPTION': 'DESCRIPTION',
    'Unnamed: 6_level_0_CATEGORY': 'CATEGORY'
}, inplace=True)

# Drop rows where all values are missing
df = df.dropna(how="all")

# Inspect the cleaned column names after flattening
print("After cleaning column names:")
print(df.head())

# Define the output file path
output_file_path = os.path.join(output_folder_path, "flattened_data.csv")

# Save the cleaned dataset
df.to_csv(output_file_path, index=False)

# Confirm the file has been saved
print(f"Flattened data saved to: {output_file_path}")