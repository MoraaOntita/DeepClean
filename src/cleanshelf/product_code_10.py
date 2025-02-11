import pandas as pd
import json
import os

# Define paths
input_file = "artifacts/cleanshelf/product_description/updated_product_descriptions.csv"
output_folder = "artifacts/cleanshelf/product_code"
output_file = os.path.join(output_folder, "final_product_codes.csv")

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Product codes mapping
product_codes = {
    "FPADCCS": "Mikalla Anti-dandruff Shampoo",
    "FPADHC150GM": "Mikalla Anti-dandruff Crème 150g",
    "FPADHC275GM": "Mikalla Anti-dandruff Crème 275g",
    "FPADHC75GM": "Mikalla Anti-dandruff Crème 75g",
    "FPALL155ML": "H&B Argan&Lavender Lotion 155ML",
    "FPALL280ML": "H&B Argan&Lavender Lotion 280ML",
    "FPALL420ML": "H&B Argan&Lavender Lotion 420ML",
    "FPBBL155ML": "H&B Berry Blossom Lotion 155ML",
    "FPBBL280ML": "H&B Berry Blossom Lotion 280ML",
    "FPBBL420ML": "H&B Berry Blossom Lotion 420ML",
    "FPBF300GM": "H&B Berry Fusion Body Scrub 300GM-DEACTIVATED",
    "FPBF700GM": "H&B Berry Fusion Body Scrub 700GM-DEACTIVATED",
    "FPBFS300GM": "H&B Berry Fusion Scrub 300g",
    "FPBFS700GM": "H&B Berry Fusion Scrub 700g",
    "FPBS120ML": "Mikalla 5in1 Braid Spray 120ml",
    "FPBS250ML": "Mikalla 5in1 Braid Spray 250ml",
    "FPBS65ML": "Mikalla 5in1 Braid Spray 65ml",
    "FPCAG150GM": "Mikalla Curl Activator Gel 150g",
    "FPCAG250GM": "Mikalla Curl Activator Gel 250g",
    "FPCAG450GM": "Mikalla Curl Activator Gel 450g",
    "FPCBL155ML": "H&B Cocoa Butter Lotion 155ML",
    "FPCBL280ML": "H&B Cocoa Butter Lotion 280ML",
    "FPCBL420ML": "H&B Cocoa Butter Lotion 420ML",
    "FPCCS1000ML": "Mikalla Shampoo 1litre",
    "FPCCS450ML": "Mikalla Shampoo 450ml",
    "FPCCS5000ML": "Mikalla Shampoo 5litre",
    "FPCCS65ML": "Mikalla Shampoo 65ml (Sample)",
    "FPCDCCS": "Mikalla Charcoal Detox Shampoo",
    "FPCVS300GM": "H&B Coffee Vanilla Scrub 300g",
    "FPCVS700GM": "H&B Coffee Vanilla Scrub 700g",
    "FPDCK240ML": "Mikalla Detangling Conditioner Kids 240ml",
    "FPECG250G": "Mikalla Edge Control Gel Kids 250g",
    "FPEML155ML": "H&B Epic Man Lotion 155ML",
    "FPEML280ML": "H&B Epic Man Lotion 280ML",
    "FPEML420ML": "H&B Epic Man Lotion 420ML",
    "FPHBC1000ML": "Mikalla Honey & Butter Conditioner 1litre",
    "FPHBC450ML": "Mikalla Honey & Butter Conditioner 450ml",
    "FPHBC5000ML": "Mikalla Honey & Butter Conditioner 5litre",
    "FPHBC65ML": "Mikalla Honey & Butter Conditioner 65ml (Sample)",
    "FPHFSS150GM": "Mikalla Scalp Soother Hairfood 150g",
    "FPHFSS250GM": "Mikalla Scalp Soother Hairfood 250g",
    "FPHFSS400GM": "Mikalla Scalp Soother Hairfood 400g",
    "FPHFSS75GM": "Mikalla Scalp Soother Hairfood 75g",
    "FPHMT1100GM": "Mikalla Mayonnaise Treatment 1100g",
    "FPHMT261GM": "Mikalla Mayonnaise Treatment 261g",
    "FPHMT407GM": "Mikalla Mayonnaise Treatment 407g",
    "FPHMT700G": "Mikalla Mayonnaise Treatment 700g",
    "FPLT1000ML": "Mikalla Leave-In Treatment 1litre",
    "FPLT100ML": "Mikalla Leave-In Treatment 100ml",
    "FPLT250ML": "Mikalla Leave-In Treatment 250ml",
    "FPLT450ML": "Mikalla Leave-In Treatment 450ml",
    "FPLT65ML": "Mikalla Leave-In Treatment 65ml (Sample)",
    "FPLTK240ML": "Mikalla Leave-in Treatment Kids 240ml",
    "FPMTK250G": "Mikalla Deep moisture treatment Kids 250g",
    "FPNHF150GM": "Mikalla Nourishing Hair Food 150g",
    "FPNHF250GM": "Mikalla Nourishing Hair Food 250g",
    "FPNHF400GM": "Mikalla Nourishing Hair Food 400g",
    "FPNHF75GM": "Mikalla Nourishing Hair Food 75g",
    "FPOEL155ML": "H&B Oatmeal Extract Lotion 155ML",
    "FPOEL280ML": "H&B Oatmeal Extract Lotion 280ML",
    "FPOEL420ML": "H&B Oatmeal Extract Lotion 420ML",
    "FPQT1000GM": "Mikalla Quadra Oil Treatment 1kg",
    "FPQT150GM": "Mikalla Quadra Oil Treatment 150g",
    "FPQT250GM": "Mikalla Quadra Oil Treatment 250g",
    "FPQT400GM": "Mikalla Quadra Oil Treatment 400g",
    "FPQT700GM": "Mikalla Quadra Oil Treatment 700g",
    "FPSBL155ML": "H&B Shea Butter Lotion 155ML",
    "FPSBL280ML": "H&B Shea Butter Lotion 280ML",
    "FPSBL420ML": "H&B Shea Butter Lotion 420ML",
    "FPSFCCS": "Mikalla sulphate free Shampoo",
    "FPSG150GM": "Mikalla Styling Gel 150g",
    "FPSG250GM": "Mikalla Styling Gel 250g",
    "FPSG450GM": "Mikalla Styling Gel 450g",
    "FPTFKS250ML": "Mikalla Tear Free Kids Shampoo 250ml",
    "FPVSCCS": "Mikalla Volume + Strength Shampoo"
  }
  
# Read input file
df = pd.read_csv(input_file)

# Create a reverse lookup dictionary
description_to_code = {v: k for k, v in product_codes.items()}

# Assign product codes
df["product_code"] = df["Product_Desc"].map(description_to_code)

# Save output
df.to_csv(output_file, index=False)

print(f"File saved: {output_file}")
