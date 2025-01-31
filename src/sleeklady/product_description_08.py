import pandas as pd
import json
import os
import sys
import logging

# Add the src folder to sys.path to ensure it can find sleeklady
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, root_dir)

from sleeklady.configurations.config import CONFIG  # Import CONFIG from the correct location

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s: %(levelname)s: %(message)s]")
logger = logging.getLogger(__name__)

# Load paths from config.yaml
csv_file_path = os.path.join(CONFIG["paths"]["columns_created"], CONFIG["files"]["columns_added_csv"])
json_file_path = CONFIG["files"]["product_description_json"]  # Direct reference
output_folder = CONFIG["paths"]["product_description_folder"]  # ✅ Corrected
output_file_path = os.path.join(output_folder, CONFIG["files"]["updated_product_descriptions_csv"])

def load_csv(file_path):
    """Load the CSV file into a pandas DataFrame."""
    try:
        logger.info(f"Loading CSV file: {file_path}")
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {e}")
        raise

def load_json(file_path):
    """Load the JSON file into a dictionary."""
    try:
        logger.info(f"Loading JSON file: {file_path}")
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {file_path} - {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading JSON file: {file_path} - {e}")
        raise

def main():
    try:
        # Load the CSV file
        data = load_csv(csv_file_path)

        # Load the JSON file with product mappings
        product_mapping = load_json(json_file_path)

        # Function to replace product descriptions using the mapping
        def replace_product_description(description):
            return product_mapping.get(description, description)

        # Replace the product descriptions in the DataFrame
        if "ProductDescriptions" in data.columns:
            data["ProductDescriptions"] = data["ProductDescriptions"].apply(replace_product_description)
        else:
            logger.warning("The 'ProductDescriptions' column is missing in the CSV file.")
            return

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the updated DataFrame to a new CSV file
        data.to_csv(output_file_path, index=False)
        logger.info(f"Updated file saved to: {output_file_path}")

    except Exception as e:
        logger.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
