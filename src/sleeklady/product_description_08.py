import os
import sys
import pandas as pd
import json
from typing import Callable
from sleeklady.configurations.config import CONFIG
from sleeklady import logger


def log_function_call(func: Callable) -> Callable:
    """Decorator to log function calls and exits."""
    def wrapper(*args, **kwargs):
        logger.info(f"Entering {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper


@log_function_call
def load_csv(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {str(e)}")
        raise


@log_function_call
def load_json(file_path: str) -> dict:
    """Load a JSON file with product descriptions."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to load JSON file: {file_path} - {str(e)}")
        raise


@log_function_call
def replace_product_description(description: str, product_mapping: dict) -> str:
    """Replace product descriptions using the provided mapping."""
    return product_mapping.get(description, description)


@log_function_call
def create_directory(directory_path: str) -> None:
    """Create the directory if it doesn't exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"Directory created at: {directory_path}")
    except Exception as e:
        logger.error(f"Failed to create directory: {directory_path} - {str(e)}")
        raise


@log_function_call
def save_to_csv(df: pd.DataFrame, output_file_path: str) -> None:
    """Save the DataFrame to a CSV file."""
    try:
        df.to_csv(output_file_path, index=False)
        logger.info(f"Data saved to: {output_file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {output_file_path} - {str(e)}")
        raise


def main():
    """Main function to load data, replace product descriptions, and save the updated file."""
    try:
        # Define the paths from the configuration
        input_file_path = os.path.join(CONFIG['paths']['columns_created'], 'columns_added.csv')
        product_mapping_file = os.path.join(CONFIG['paths']['product_description'], 'product_description.json')  # Updated path
        output_folder = CONFIG['paths']['product_description']

        # Load the CSV and JSON files
        data = load_csv(input_file_path)
        product_mapping = load_json(product_mapping_file)

        # Replace the product descriptions
        data['ProductDescriptions'] = data['ProductDescriptions'].apply(replace_product_description, args=(product_mapping,))

        # Create the output directory
        create_directory(output_folder)

        # Define the output file path
        output_file_path = os.path.join(output_folder, 'updated_product_descriptions.csv')

        # Save the updated data to a new CSV file
        save_to_csv(data, output_file_path)

        print(f"Updated file saved to: {output_file_path}")

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
