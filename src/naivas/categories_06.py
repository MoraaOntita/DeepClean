import pandas as pd
import re
import os

# Define file paths
input_file = r'artifacts\naivas\brands\brands.csv'
output_folder = r'artifacts\naivas\categories'
output_file = os.path.join(output_folder, 'categorized_data.csv')

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the dataset
df = pd.read_csv(input_file)

# Define categories and their corresponding regex patterns
categories = {
    "Hair Treatment": r"(treatment|treat|trt|mayonnaise|T-MENT|BOOSTLEAVE)",
    "Hair Shampoo": r"(clen&cond shamp|clen|shampoo|shamp|charc dtx sham|cleans&cond shamp)", 
    "Hair Conditioner": r"(conditioner|cond)",
    "Hair Food": r"(scalp soother|s/soother|h/food|anti dandruff creme|anti dandruff crm|crm)",
    "Hair Gel": r"(gels|gel|curl activator)",
    "Hair Spray": r"spray",
    "Body Lotion": r"(lotion|b/ltn)",
    "Body Scrub": r"(scrub|b/scrub)"
}

# Function to categorize products
def categorize_product(desc):
    for category, pattern in categories.items():
        if pd.notna(desc) and re.search(pattern, str(desc), re.IGNORECASE):
            return category
    return "Other"  # Default if no match is found

# Apply categorization
df['Categories'] = df['DESCRIPTION'].apply(categorize_product)

# Save the modified DataFrame
df.to_csv(output_file, index=False)

print(f"Categorized data saved to: {output_file}")
