import pandas as pd
import os

# Input and output file paths
input_file = "artifacts/naivas/product_code/final_product_codes.csv"
output_folder = "artifacts/naivas/capitalized"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "capitalized_final_product_codes.csv")

# Load data
df = pd.read_csv(input_file, dtype=str)  # Ensure all columns are read as strings

# Capitalize all data
df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Save the capitalized DataFrame
df.to_csv(output_file, index=False)

print(f"Capitalized file successfully saved at: {output_file}")