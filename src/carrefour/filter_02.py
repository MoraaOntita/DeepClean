import os
import sys
import pandas as pd
from typing import Optional


# Add the src folder to sys.path to ensure it can find sleeklady
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)

from src.carrefour import logger
from src.carrefour.configurations.config import CONFIG

def log_function_call(func):
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
def get_csv_file_path() -> str:
    """Get the full path of the CSV file."""
    return os.path.join(CONFIG['paths']['formatted_folder'], 'CarrefourDataEncodingFree.csv')


@log_function_call
def read_csv_file(file_path: str) -> pd.DataFrame:
    """Read the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to read CSV file: {file_path} - {str(e)}")
        raise


@log_function_call
def filter_data(data: pd.DataFrame, supplier_name: str) -> pd.DataFrame:
    """Filter rows by supplier name."""
    return data[data['SupplierName'] == supplier_name]


@log_function_call
def create_folder(folder_path: str) -> None:
    """Create a folder if it doesn't exist."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        logger.info(f"Folder created at: {folder_path}")
    except Exception as e:
        logger.error(f"Failed to create folder {folder_path}: {str(e)}")
        raise


@log_function_call
def save_filtered_data(data: pd.DataFrame, file_path: str) -> None:
    """Save the filtered data to a CSV file."""
    try:
        data.to_csv(file_path, index=False)
        logger.info(f"Filtered data saved as CSV: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save filtered data to CSV: {str(e)}")
        raise


def main():
    """Main function to execute the filtering process."""
    try:
        # Get the file path for the CSV file
        csv_file_path = get_csv_file_path()

        # Read the CSV file
        data = read_csv_file(csv_file_path)

        # Filter the data for ALKHEMY BRANDS
        alkhemy_data = filter_data(data, 'ALKHEMY BRANDS LIMITED')

        # Get the folder path for saving filtered data
        filtered_folder_path = CONFIG['paths']['filtered_folder']
        create_folder(filtered_folder_path)

        # Define the file path for the filtered CSV file
        filtered_csv_file_path = os.path.join(filtered_folder_path, 'alkhemy_brands_data.csv')

        # Save the filtered data to a CSV file
        save_filtered_data(alkhemy_data, filtered_csv_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the filtering process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()