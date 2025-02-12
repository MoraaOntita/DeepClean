import os
import pandas as pd

# Get the root directory relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_file = os.path.join(BASE_DIR, "artifacts", "carrefour", "store_name", "store_names_transformed.csv")
output_dir = os.path.join(BASE_DIR, "artifacts", "carrefour", "total_sales")
output_file = os.path.join(output_dir, "totalsales.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Rename the 'Values' column to 'Quantity' (if not already renamed)
df.rename(columns={"Item Name": "ProductDescriptions"}, inplace=True)

# Calculate TotalSales
# Avoid division by zero and handle missing values
df["TotalSales"] = (df["Unnamed: 51"] / df["Unnamed: 50"]).fillna(0).replace([float("inf"), -float("inf")], 0) * df["Quantity"]

# Round the TotalSales column to 2 decimal places
df["TotalSales"] = df["TotalSales"].round(2)

# Drop the 'Unnamed: 51' and 'Unnamed: 50' columns
df.drop(columns=["Unnamed: 51", "Unnamed: 50"], inplace=True)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
