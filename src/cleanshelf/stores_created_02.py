import os
import pandas as pd

# Define file paths
root_dir = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI"
input_file = os.path.join(root_dir, "artifacts/cleanshelf/formatted/formatted_data.csv")
output_dir = os.path.join(root_dir, "artifacts/cleanshelf/filtered")
output_file = os.path.join(output_dir, "reshaped_data.csv")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Step 1: Load the data
try:
    # Skip extra rows and load data
    data = pd.read_csv(input_file, header=[0, 1])  # Adjust header rows if needed
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Step 2: Reshape the data
# Define the store columns (Sold Qty and Value pairs)
store_columns = [
    ("COVO-LAVINGTON", "Sold Qty"), ("COVO-LAVINGTON", "Value"),
    ("FRESHMARKET", "Sold Qty"), ("FRESHMARKET", "Value"),
    ("GREEN PARK", "Sold Qty"), ("GREEN PARK", "Value"),
    ("KAHAWA WEST", "Sold Qty"), ("KAHAWA WEST", "Value"),
    ("KERUGOYA", "Sold Qty"), ("KERUGOYA", "Value"),
    ("KIAMBU", "Sold Qty"), ("KIAMBU", "Value"),
    ("KIKUYU", "Sold Qty"), ("KIKUYU", "Value"),
    ("K-MALL", "Sold Qty"), ("K-MALL", "Value"),
    ("LANGATA", "Sold Qty"), ("LANGATA", "Value"),
    ("LIMURU", "Sold Qty"), ("LIMURU", "Value"),
    ("NAKURU", "Sold Qty"), ("NAKURU", "Value"),
    ("NGONG", "Sold Qty"), ("NGONG", "Value"),
    ("NYAHURURU", "Sold Qty"), ("NYAHURURU", "Value"),
    ("RONGAI", "Sold Qty"), ("RONGAI", "Value"),
    ("RUAKA", "Sold Qty"), ("RUAKA", "Value"),
    ("SOUTH B", "Sold Qty"), ("SOUTH B", "Value"),
    ("WENDANI", "Sold Qty"), ("WENDANI", "Value")
]

# Melt the DataFrame to unpivot the store columns
reshaped_data = data.melt(
    id_vars=["Supp Name"],  # Keep supplier name
    value_vars=store_columns,
    var_name=["StoreNames", "Metric"],
    value_name="Value"
)

# Step 3: Clean up the reshaped data
reshaped_data = reshaped_data.pivot_table(
    index=["Supp Name", "StoreNames"],
    columns="Metric",
    values="Value",
    aggfunc="first"
).reset_index()

# Step 4: Save the reshaped data
reshaped_data.to_csv(output_file, index=False)
print(f"Reshaped data saved to {output_file}")
