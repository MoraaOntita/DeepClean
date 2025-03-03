import os
import pandas as pd

# Get the root directory relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_file = os.path.join(BASE_DIR, "artifacts", "carrefour", "categories", "categories.csv")
output_dir = os.path.join(BASE_DIR, "artifacts", "carrefour", "columns_created")
output_file = os.path.join(output_dir, "created_columns.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Add new columns with static values
df["AccountName"] = "Majid AL Futtaim Hypermarkets Ltd"
df["Group"] = "MT"
df["SalesRep"] = "Leah"
df["Date"] = "Jan25"
df["AccountCode"] = "MAJ004"


# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"File with new columns saved successfully at: {output_file}")
