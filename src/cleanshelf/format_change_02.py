import os
import pandas as pd

# Define the relative paths
input_file_path = "artifacts/cleanshelf/headers/cleaned_data.xlsx"
output_folder_path = "artifacts/cleanshelf/formatted"

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Load the Excel file
df = pd.read_excel(input_file_path, header=[0, 1])  # Read first two rows as headers

# Inspect the first few rows before cleaning column names
print("Before cleaning column names:")
print(df.head())

# Clean column names by combining multi-level columns and removing 'Unnamed' part
df.columns = [
    "_".join([str(col[0]), str(col[1])]) if isinstance(col, tuple) else col 
    for col in df.columns
]

# Inspect the cleaned column names after flattening
print("After cleaning column names:")
print(df.head())

# Manually rename the columns to the correct names
df.rename(columns={
    'Unnamed: 0_level_0_Product Code': 'Product Code',
    'Unnamed: 1_level_0_Product Desc': 'Product Desc',
    'Unnamed: 2_level_0_Dept Name': 'Dept Name',
    'Unnamed: 3_level_0_Class Name': 'Class Name',
    'Unnamed: 4_level_0_Supp Name': 'Supp Name'
}, inplace=True)

# Inspect the renamed column names
print("After renaming column names:")
print(df.head())

# Proceed with cleaning: dropping duplicates, handling missing values, etc.
df = df.dropna(how="all")  # Drop rows where all values are missing

# Define the output file path
output_file_path = os.path.join(output_folder_path, "cleaned_data.csv")

# Save the cleaned dataset
df.to_csv(output_file_path, index=False)

# Confirm the file has been saved
print(f"Cleaned data saved to: {output_file_path}")
