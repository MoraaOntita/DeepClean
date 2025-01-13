import pandas as pd

# Define the file paths
input_file_path = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf/formatted_data.csv"
output_file_path = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf/formatted_to_long_transformed_data.csv"

# Read the CSV file
df = pd.read_csv(input_file_path)

# Define the columns that represent the store names
store_columns = [
    "FRESH MARKET", "GREEN PARK", "KAHAWA WEST", "KERUGOYA", "KIAMBU", "KIKUYU",
    "K-MALL", "LANGATA", "LIMURU", "NAKURU", "NYAHURURU", "RONGAI", "RUAKA", "WENDANI"
]

# Melt the dataframe from wide to long format
long_df = pd.melt(
    df,
    id_vars=["Product Code", "Product Description", "Total Quantity", "Discount", "Total Discount"],
    value_vars=store_columns,
    var_name="Store Name",
    value_name="Quantity"
)

# Replace NaN values in the Quantity column with 0
long_df["Quantity"] = long_df["Quantity"].fillna(0)

# Convert Quantity to integer type (optional, if appropriate)
long_df["Quantity"] = long_df["Quantity"].astype(int)

# Drop rows where Quantity is 0
filtered_long_df = long_df[long_df["Quantity"] > 0].copy()

# Optional: Reset the index after filtering
filtered_long_df.reset_index(drop=True, inplace=True)

# Save the transformed and filtered data to a new CSV file with a descriptive name
filtered_output_path = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf/created_stores.csv"
filtered_long_df.to_csv(filtered_output_path, index=False)

print(f"Transformed and filtered data saved to: {filtered_output_path}")
