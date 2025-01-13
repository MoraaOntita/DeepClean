import pandas as pd

# File paths
input_file_path = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf/created_stores.csv"
output_file_path = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf/dropped_columns.csv"

# Read the CSV file
df = pd.read_csv(input_file_path)

# Columns to drop
columns_to_drop = ["Product Code", "Total Quantity", "Total Discount", "Discount"]

# Drop the specified columns
filtered_df = df.drop(columns=columns_to_drop, errors="ignore")

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file_path, index=False)

print(f"Filtered file saved to: {output_file_path}")
