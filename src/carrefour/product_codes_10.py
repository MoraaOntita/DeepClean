import os
import pandas as pd
import json
import sys

# Add the src folder to sys.path to ensure it can find sleeklady
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)

from src.carrefour.configurations.config import CONFIG



def load_json(file_path: str) -> dict:
    """Load a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {file_path} - {e}")
        raise


def get_product_code(description: str, product_codes: dict) -> str:
    """Return the product code from the description."""
    return {v: k for k, v in product_codes.items()}.get(description, None)


def create_directory(directory_path: str) -> None:
    """Create the directory if it doesn't exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory created at: {directory_path}")
    except Exception as e:
        print(f"Error creating directory: {directory_path} - {e}")
        raise


def save_to_csv(df: pd.DataFrame, output_file_path: str) -> None:
    """Save a pandas DataFrame to a CSV file."""
    try:
        df.to_csv(output_file_path, index=False)
        print(f"Data saved to: {output_file_path}")
    except Exception as e:
        print(f"Error saving CSV file: {output_file_path} - {e}")
        raise


def process_product_codes():
    """Main function to process product codes."""
    # Get base directory
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Define relative paths
    input_file_path = os.path.join(BASE_DIR, "artifacts", "carrefour", "product_description", "product_description.csv")
    product_codes_file = os.path.join(BASE_DIR, "src", "carrefour", "configurations", "product_codes.json")

    # Load data
    data = pd.read_csv(input_file_path)
    product_codes = load_json(product_codes_file)

    # Create a new column 'product_code' using the 'ProductDescriptions' column
    data['product_code'] = data['ProductDescriptions'].apply(get_product_code, args=(product_codes,))

    # Automatically create the folder if it doesn't exist
    output_folder = os.path.join(BASE_DIR, CONFIG['paths']['product_code'])
    create_directory(output_folder)

    # Save the updated DataFrame to a new CSV file
    output_file_path = os.path.join(output_folder, 'updated_product_codes.csv')
    save_to_csv(data, output_file_path)

    print(f"Updated file with product codes saved to: {output_file_path}")


if __name__ == "__main__":
    process_product_codes()
