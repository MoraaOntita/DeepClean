import os
import sys
import pandas as pd
import re
from typing import Callable
import json

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)

from src.sleeklady import logger
from src.sleeklady.configurations.config import CONFIG


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
def get_file_path(file_name: str) -> str:
    """Resolve the full path for the brands CSV file from the configuration."""
    return os.path.join(CONFIG['paths']['brands_folder'], file_name)


@log_function_call
def load_csv(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {str(e)}")
        raise


@log_function_call
def load_store_mapping() -> dict:
    """Load store name mapping from the JSON file."""
    try:
        store_mapping_path = CONFIG['files']['store_mapping_json']
        with open(store_mapping_path, 'r') as file:
            store_mapping = json.load(file)
        return store_mapping
    except Exception as e:
        logger.error(f"Failed to load store name mapping: {str(e)}")
        raise


@log_function_call
def replace_store_name(store_name: str, store_mapping: dict) -> str:
    """Replace the entire cell content with the mapped store name based on the store ID."""
    store_name_pattern = CONFIG['patterns']['store_name_pattern']  # Get the pattern from config
    
    match = re.search(store_name_pattern, store_name, re.IGNORECASE)

    if match:
        store_id = match.group(0)  # Extract the store ID
        # Fetch the full store name from the mapping
        full_store_name = store_mapping.get(store_id)
        if full_store_name:
            return full_store_name  # Replace the entire cell with the mapped store name
    
    # If no match is found or mapping fails, return the original store_name
    return store_name


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
def save_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """Save the DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        logger.info(f"Data saved to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {file_path} - {str(e)}")
        raise


@log_function_call
def combine_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Combine duplicate rows by summing the 'Quantity' and 'TotalSellingPrice' columns."""
    return df.groupby(['ProductDescriptions', 'StoreNames', 'Brands', 'Categories'], as_index=False).agg({
        'Quantity': 'sum',
        'TotalSellingPrice': 'sum'
    })


def main():
    """Main function to process the CSV and replace store names."""
    try:
        # Load the store mapping from the JSON file
        store_mapping = load_store_mapping()

        # Get the full path of the CSV file from config
        file_path = get_file_path(CONFIG['files']['brands_csv'])

        # Load the dataset
        df = load_csv(file_path)

        # Apply the function to the 'StoreNames' column using the store mapping
        df['StoreNames'] = df['StoreNames'].apply(lambda store_name: replace_store_name(store_name, store_mapping))

        # Combine duplicate rows
        df_combined = combine_duplicates(df)

        # Resolve the output folder path from the configuration
        output_folder = CONFIG['paths']['store_folder']
        create_directory(output_folder)

        # Define the output file path for saving the modified dataset
        output_file_path = os.path.join(output_folder, CONFIG['files']['modified_with_resolved_store_names_csv'])

        # Save the updated dataset to the specified file path
        save_to_csv(df_combined, output_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
