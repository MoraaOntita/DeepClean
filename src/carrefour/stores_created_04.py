import os
import pandas as pd

# Get the root directory relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_file = os.path.join(BASE_DIR, "artifacts", "carrefour", "dropped_columns", "alkhemy_brands_dropped_columns.csv")
output_dir = os.path.join(BASE_DIR, "artifacts", "carrefour", "store_name")
output_file = os.path.join(output_dir, "store_names_transformed.csv")

# Load the CSV file
df = pd.read_csv(input_file)

# Define the store columns
store_columns = [
    "3110 - KRIV", "3111 - KHUB", "3112 - KBBY", "3118 - KSOF", "3119 - KIRU", "3120 - KTRM",
    "3123 - KMGA", "3126 - KGLR", "3133 - KKI1", "8122 - KJCN", "8124 - KSRT", "8114 - KXGCM", "8115 - KXWGT",
    "8116 - KXNGN", "8117 - KXVYA", "8119 - KXKLM", "8121 - KXKEC", "8123 - KXCTH", "8128 - KXVLM", 
    "8131 - KXNCM", "8139 - KXDIN", "8140 - XKEF", "8142 - XKEH", "8151 - XKEG", "8156 - XKEQ", "8148 - XKEI", 
    "8144 - XKEL"
]

# Define the store mapping dictionary
store_mapping = {
    "3110 - KRIV": "Two Rivers",
    "3111 - KHUB": "Nairobi Hub",
    "3112 - KBBY": "Business Bay",
    "3118 - KSOF": "SouthField",
    "3119 - KIRU": "Ruiru Nord",
    "3120 - KTRM": "TRM",
    "3123 - KMGA": "Mega",
    "3126 - KGLR": "Galleria",
    "3133 - KKI1": "United Mall",
    "8122 - KJCN": "The Junction",
    "8124 - KSRT": "Sarit Center",
    "8114 - KXGCM": "Garden City",
    "8115 - KXWGT": "Westgate",
    "8116 - KXNGN": "NextGen",
    "8117 - KXVYA": "Valley Arcade",
    "8119 - KXKLM": "Kilimani",
    "8121 - KXKEC": "St Ellies",
    "8123 - KXCTH": "Comet House",
    "8128 - KXVLM": "Village Market",
    "8131 - KXNCM": "Mom Nyali Complex",
    "8139 - KXDIN": "Mom Diani",
    "8144 - XKEL": "Rhaphta Promenade",
    "8140 - XKEF": "Mom Promenade",
    "8142 - XKEH": "Runda",
    "8151 - XKEG": "GTC",
    "8156 - XKEQ": "Spring Valley",
    "8148 - XKEI": "Rubis Makutano",
    
}

# Melt the DataFrame to move store columns under 'StoreNames'
df_melted = df.melt(id_vars=[col for col in df.columns if col not in store_columns],
                    value_vars=store_columns,
                    var_name="StoreNames",
                    value_name="Quantity")

# Replace store codes with actual store names
df_melted["StoreNames"] = df_melted["StoreNames"].map(store_mapping)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the modified DataFrame
df_melted.to_csv(output_file, index=False)

print(f"File saved successfully at: {output_file}")
