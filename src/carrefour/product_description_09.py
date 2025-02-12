import pandas as pd
import json
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s: %(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get the root directory relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_csv_path = os.path.join(BASE_DIR, "artifacts", "carrefour", "columns_created", "created_columns.csv")
json_file_path = os.path.join(BASE_DIR, "src", "carrefour", "configurations", "product_description.json")
output_file_path = os.path.join(BASE_DIR, "artifacts", "carrefour", "product_description", "product_description.csv")

# Load CSV file
def load_csv(file_path):
    try:
        logging.info(f"Loading CSV file from {file_path}")
        df = pd.read_csv(file_path)
        logging.info("CSV file loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to load CSV file: {e}")
        raise

# Load JSON file
def load_json(file_path):
    try:
        logging.info(f"Loading JSON file from {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        logging.info("JSON file loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON file: {e}")
        raise

# Replace product descriptions
def replace_product_descriptions(df, mapping):
    try:
        logging.info("Replacing product descriptions...")
        if 'ProductDescriptions' not in df.columns:
            raise KeyError("Column 'ProductDescriptions' not found in the CSV file.")
        df['ProductDescriptions'] = df['ProductDescriptions'].apply(lambda desc: mapping.get(desc, desc))
        logging.info("Product descriptions replaced successfully.")
        return df
    except Exception as e:
        logging.error(f"Error during replacement: {e}")
        raise

# Save updated CSV file
def save_csv(df, file_path):
    try:
        logging.info(f"Saving updated CSV file to {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if it doesn't exist
        df.to_csv(file_path, index=False)
        logging.info("Updated CSV file saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save updated CSV file: {e}")
        raise

# Main function
def main():
    try:
        # Load data
        df = load_csv(input_csv_path)
        mapping = load_json(json_file_path)

        # Replace descriptions
        updated_df = replace_product_descriptions(df, mapping)

        # Save updated file
        save_csv(updated_df, output_file_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
