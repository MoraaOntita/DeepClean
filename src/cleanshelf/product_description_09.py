import pandas as pd
import os

# File paths
input_file = r"artifacts\cleanshelf\columns_created\columns_added_data.csv"
output_folder = r"artifacts\cleanshelf\product_description"
output_file = os.path.join(output_folder, "updated_product_descriptions.csv")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load data
df = pd.read_csv(input_file)

# Define the mapping of old product names to new names
product_mapping = {
    "MIKALLA MAYONNAISE T-MENT 261GM": "Mikalla Mayonnaise Treatment 261g",


    "MIKALLA QUADRA OIL TREAT 150G": "Mikalla Quadra Oil Treatment 150g",
    "MIKALLA QUADRA OIL TREAT 250G": "Mikalla Quadra Oil Treatment 250g",    
    "MIKALLA QUADRA OIL TREAT 400G": "Mikalla Quadra Oil Treatment 400g",  


    "MIKALLA MOIST BOOSTLEAVE 100ML": "Mikalla Leave-In Treatment 100ml",
    "MIKALLA MOIST BOOSTLEAVE 250ML": "Mikalla Leave-In Treatment 250ml",
    "MIKALLA MOIST BOOSTLEAVE 450ML": "Mikalla Leave-In Treatment 450ml",      
    

    "MIKALLA STYLING GEL 150GM": "Mikalla Styling Gel 150g",

    "MIKALLA HNY&BUTTER COND 450ML": "Mikalla Honey & Butter Conditioner 450ml",


    "MIKALLA CLEANS&COND SHAMP 450ML": "Mikalla Shampoo 450ml",

    "MIKALLA NOURISHING H/FOOD 75G": "Mikalla Nourishing Hair Food 75g",
    
    "MIKALLA SCALP SOOTHER 150GM ": "Mikalla Scalp Soother Hairfood 150g",
    "MIKALLA SCALP SOOTHER 75GM ": "Mikalla Scalp Soother Hairfood 75g",


    "MIKALLA ANTI-DANDRUFF CRM 150G": "Mikalla Anti-dandruff Cream 150g",
    "MIKALLA ANTI-DANDRUFF CRM 75G": "Mikalla Anti-dandruff Cream 75g",


    "MIKALLA 5IN1 BRAID SPRAY 120ML": "Mikalla 5in1 Braid Spray 120ml",
    "MIKALLA 5IN1 BRAID SPRAY 250ML": "Mikalla 5in1 Braid Spray 250ml",

    
    "MIKALLA HONEY&BUTTER BERRY FUSION BODY SCRUB 300GM ": "H&B Berry Fusion Scrub 300g",
    "MIKALLA HONEY&BUTTER COFFEE&VANILLA BODY SCRUB 300GM": "H&B Coffee Vanilla Scrub 300g",

}

# Apply the mapping to the 'Product_Desc' column
df["Product_Desc"] = df["Product_Desc"].replace(product_mapping)

# Save the updated DataFrame
df.to_csv(output_file, index=False)

print(f"Updated file saved at: {output_file}")
