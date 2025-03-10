import pandas as pd
import os
import csv

# File paths
input_file = r"artifacts\naivas\categories\categorized_data.csv"
output_folder = r"artifacts\naivas\columns_created"
output_file = os.path.join(output_folder, "columns_added_data.csv")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the data
df = pd.read_csv(input_file, dtype=str)  # Force all columns to be strings

# Add new columns
df["Account_Name"] = "Naivas Supermarkets Ltd"
df["Group"] = "mt"
df["Sales_Rep"] = "leah"
df["Date"] = "Feb25"  # Keep it as a string without apostrophe
df["Account_code"] = "NAI003"



# Save as CSV without extra formatting issues
df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)  # Ensures text stays as is

print(f"Updated data saved to: {output_file}")
