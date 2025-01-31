import os
import pandas as pd

# Define file paths
root_dir = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI"
input_file = os.path.join(root_dir, "artifacts/cleanshelf/formatted/formatted_data.csv")
output_dir = os.path.join(root_dir, "artifacts/cleanshelf/filtered")
output_file = os.path.join(output_dir, "filtered_data.csv")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Step 1: Load the data with careful header handling
try:
    # Load the file, skipping rows that don't form part of the header
    data = pd.read_csv(input_file, header=[1, 2], skiprows=0)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Step 2: Flatten multi-level headers
data.columns = ['_'.join(col).strip() for col in data.columns.values]

# Step 3: Drop empty or irrelevant columns
data = data.dropna(how="all", axis=1)  # Drop columns where all values are NaN

# Step 4: Filter rows for "ALKHEMY BRANDS LIMITED"
filtered_data = data[data["Supp Name"] == "ALKHEMY BRANDS LIMITED"]

# Step 5: Save the cleaned and filtered data
filtered_data.to_csv(output_file, index=False)
print(f"Filtered data saved to {output_file}")
