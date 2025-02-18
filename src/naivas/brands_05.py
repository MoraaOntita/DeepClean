import pandas as pd
import os

# Define file paths
input_file = r'artifacts\naivas\dropped\cleaned_column_final.csv'
output_folder = r'artifacts\naivas\brands'
output_file = os.path.join(output_folder, 'brands.csv')

# Load the dataset
df = pd.read_csv(input_file)

# Function to categorize brands based on DESCRIPTION
def classify_brand(desc):
    desc = str(desc).lower()  # Convert to lowercase for case-insensitive matching
    
    # Brand classification logic
    if "scrub" in desc:
        return "H&B"
    elif "mikalla" in desc:
        return "Mikalla"
    elif any(keyword in desc for keyword in ["honey", "butter", "honey&butter"]):
        return "H&B"
    else:
        return "Other"

# Apply function to create 'brands' column
df["brands"] = df["DESCRIPTION"].apply(classify_brand)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save the updated dataset
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
