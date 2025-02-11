import pandas as pd
import os

# File paths
input_file = "artifacts/cleanshelf/dropped_columns/cleaned_data_transformed_dropped.csv"
output_folder = "artifacts/cleanshelf/brands"
output_file = os.path.join(output_folder, "cleaned_data_transformed_brands.csv")

# Load data
df = pd.read_csv(input_file)

# Function to categorize brands based on Product_Desc
# Function to categorize brands based on Product_Desc
def classify_brand(desc):
    desc = str(desc).lower()  # Convert to lowercase for case-insensitive matching
    
    # If "Scrub" is in the description, classify it as "H&B" first
    if "scrub" in desc:
        return "H&B"
    
    # Otherwise, check for Mikalla or Honey & Butter
    elif "mikalla" in desc:
        return "Mikalla"
    elif any(keyword in desc for keyword in ["honey", "butter", "honey&butter"]):
        return "H&B"
    else:
        return "Other"

# Apply function to create 'brands' column
df["brands"] = df["Product_Desc"].apply(classify_brand)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save updated DataFrame
df.to_csv(output_file, index=False)

print(f"File successfully saved at: {output_file}")
