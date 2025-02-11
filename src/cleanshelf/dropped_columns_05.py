import pandas as pd
import os

# Define file paths
input_file = "artifacts/cleanshelf/edited_columns/cleaned_data_transformed.csv"
output_folder = "artifacts/cleanshelf/dropped_columns"
output_file = os.path.join(output_folder, "cleaned_data_transformed_dropped.csv")

# List of columns to drop
columns_to_drop = ["Product_Code", "Dept_Name", "Supp_Name", "Class_Name"]

# Load the CSV file
df = pd.read_csv(input_file)

# Drop specified columns (ignore if columns are missing)
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
