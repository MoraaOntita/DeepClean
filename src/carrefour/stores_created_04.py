import os
import pandas as pd

# Define file paths
input_file = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/dropped_columns/alkhemy_brands_dropped_columns.csv"
output_dir = "/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/carrefour/store_name"
output_file = os.path.join(output_dir, "store_names_transformed.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Define the store columns
store_columns = [
    "3110 - KRIV", "3111 - KHUB", "3112 - KBBY", "3118 - KSOF", "3119 - KIRU", "3120 - KTRM",
    "3123 - KMGA", "3126 - KGLR", "3133 - KKI1", "8122 - KJCN", "8124 - KSRT", "8114 - KXGCM", "8115 - KXWGT",
    "8116 - KXNGN", "8117 - KXVYA", "8119 - KXKLM", "8121 - KXKEC", "8123 - KXCTH", "8128 - KXVLM", 
    "8131 - KXNCM", "8139 - KXDIN", "8140 - XKEF", "8142 - XKEH", "8151 - XKEG", "8156 - XKEQ", "8148 - XKEI"
]

# Melt the DataFrame to move store columns under 'StoreNames'
df_melted = df.melt(id_vars=[col for col in df.columns if col not in store_columns],
                    value_vars=store_columns,
                    var_name="StoreNames",
                    value_name="Quantity")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df_melted.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")


