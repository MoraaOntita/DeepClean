import os
import pandas as pd
import json
import sys
import logging

# Add the src folder to sys.path to ensure it can find sleeklady
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)

from src.sleeklady import logger
from src.sleeklady.configurations.config import CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s: %(levelname)s: %(message)s]')
logger = logging.getLogger(__name__)

def load_json(file_path: str) -> dict:
    """Load a JSON file."""
    try:
        logger.info(f"Loading JSON file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        logger.info("Successfully loaded JSON file")
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

def get_product_code(description: str, product_codes: dict) -> str:
    """Return the product code from the description."""
    return {v: k for k, v in product_codes.items()}.get(description, None)

def create_directory(directory_path: str) -> None:
    """Create the directory if it doesn't exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"Directory created or already exists: {directory_path}")
    except Exception as e:
        logger.error(f"Error creating directory: {directory_path} - {e}")
        raise

def save_to_csv(df: pd.DataFrame, output_file_path: str) -> None:
    """Save a pandas DataFrame to a CSV file."""
    try:
        df.to_csv(output_file_path, index=False)
        logger.info(f"Data successfully saved to: {output_file_path}")
    except Exception as e:
        logger.error(f"Error saving CSV file: {output_file_path} - {e}")
        raise

def process_product_codes():
    """Main function to process product codes."""
    try:
        logger.info("Starting product codes processing")

        # Load paths from config.yaml
        input_file_path = os.path.join(CONFIG['paths']['product_description'], CONFIG['files']['updated_product_descriptions_csv'])
        product_codes_file = os.path.join(CONFIG['paths']['product_code'], CONFIG['files']['product_codes_json'])  # Fixed key name
        output_folder = CONFIG['paths']['product_code']
        output_file_path = os.path.join(output_folder, CONFIG['files']['updated_product_codes_csv'])  # Fixed key name

        logger.info(f"Product codes file path: {product_codes_file}")

        # Load data
        logger.info(f"Loading CSV file: {input_file_path}")
        data = pd.read_csv(input_file_path)
        logger.info("Successfully loaded CSV file")

        # Load product codes mapping
        product_codes = load_json(product_codes_file)

        # Process data
        if 'ProductDescriptions' in data.columns:
            data['product_code'] = data['ProductDescriptions'].apply(get_product_code, args=(product_codes,))
            logger.info("Product codes successfully mapped")
        else:
            logger.warning("The 'ProductDescriptions' column is missing in the CSV file.")
            return

        # Ensure output directory exists
        create_directory(output_folder)

        # Save processed data
        save_to_csv(data, output_file_path)

        logger.info(f"Updated file with product codes saved to: {output_file_path}")

    except Exception as e:
        logger.error(f"An error occurred during product code processing: {e}")
        raise

if __name__ == "__main__":
    process_product_codes()
