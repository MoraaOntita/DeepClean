import os
import pandas as pd
import re

# Get the root directory relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_file = os.path.join(BASE_DIR, "artifacts", "carrefour", "brands", "brands.csv")
output_dir = os.path.join(BASE_DIR, "artifacts", "carrefour", "categories")
output_file = os.path.join(output_dir, "categories.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Replace '?' with 'e' in ProductDescriptions column
df["ProductDescriptions"] = df["ProductDescriptions"].str.replace("?", "E", regex=False)

# Define category mappings with regular expressions
category_mapping = {
    'Hair Treatment': r'(treatment|treat|trt|moyonnaise)',
    'Hair Shampoo': r'(clen&cond shamp|clen|shampoo|shamp|charc dtx sham)',
    'Hair Conditioner': r'(conditioner|cond)',
    'Hair Food': r'(scalp soother|s/soother|h/food|anti dandruff creme|anti dandruff crm|crm|ANTI DANDRUFF CREME)',
    'Hair Gel': r'(gels|gel|curl activator)',
    'Hair Spray': r'spray',
    'Body Lotion': r'(lotion|b/ltn)',
    'Body Scrub': r'(scrub|b/scrub|body scrub)'
}

# Helper function to assign categories based on ProductDescriptions
def assign_category(description):
    if pd.isna(description):
        return None
    for category, pattern in category_mapping.items():
        if re.search(pattern, description, flags=re.IGNORECASE):
            return category
    return "Unknown"  # Assign 'Unknown' if no category matches

# Create the 'Categories' column
df["Categories"] = df["ProductDescriptions"].apply(assign_category)

# Drop rows with any null values
df.dropna(inplace=True)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
