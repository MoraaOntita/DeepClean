import os
import pandas as pd

# Define file paths
input_file = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/total_sales/totalsales.csv"
output_dir = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/brands"
output_file = os.path.join(output_dir, "brands.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Define a dictionary mapping keywords to brands
brand_mapping = {
    "Mikalla": "Mikalla",
    "Honey": "H&B",
    "Butter": "H&B"
}

# Helper function to assign brands based on ProductDescriptions
def assign_brand(description):
    if pd.isna(description):
        return None
    for keyword, brand in brand_mapping.items():
        if keyword.lower() in description.lower():
            return brand
    return "Unknown"  # Assign 'Unknown' if no keyword matches

# Create the 'brands' column
df["brands"] = df["ProductDescriptions"].apply(assign_brand)

# Drop rows with any null values
df.dropna(inplace=True)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
