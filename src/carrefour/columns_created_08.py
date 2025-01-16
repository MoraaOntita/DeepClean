import os
import pandas as pd

# Define file paths
input_file = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/categories/categories.csv"
output_dir = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/columns_created"
output_file = os.path.join(output_dir, "created_columns.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Add new columns with static values
df["AccountName"] = "MAJ004"
df["Group"] = "MT"
df["SalesRep"] = "Leah"
df["Date"] = "Dec24"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"File with new columns saved successfully at: {output_file}")
