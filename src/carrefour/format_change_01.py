import os
import sys
import pandas as pd
import logging
from typing import Dict

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
def get_csv_file_path(root_dir: str, file_name: str) -> str:
    """Resolve the path to the CSV file."""
    return os.path.join(root_dir, CONFIG['paths']['data_folder'], file_name)

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
def check_file_exists(file_path: str) -> None:
    """Check if the file exists."""
    if not os.path.exists(file_path):
        logger.error(f"CSV file not found at: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

@log_function_call
def clean_csv(csv_file_path: str, folder_path: str) -> None:
    """Remove the first six rows from the CSV file and save the cleaned version."""
    try:
        # Load the CSV without headers, using an appropriate encoding
        df = pd.read_csv(csv_file_path, header=None, encoding="ISO-8859-1")

        # Ensure there are enough rows to remove
        if df.shape[0] > 5:
            df = df.iloc[5:].reset_index(drop=True)  # Drop first 6 rows
            df.columns = df.iloc[0]  # Set the new header from row 7
            df = df[1:].reset_index(drop=True)  # Drop the new header row from data

        cleaned_csv_path = os.path.join(folder_path, os.path.basename(csv_file_path))
        df.to_csv(cleaned_csv_path, index=False, encoding="utf-8")  # Save in UTF-8

        logger.info(f"Cleaned CSV saved: {cleaned_csv_path}")

    except Exception as e:
        logger.error(f"Failed to clean CSV {csv_file_path}: {str(e)}")
        raise

def main():
    """Main function to execute the CSV cleaning pipeline."""
    try:
        csv_file_path = get_csv_file_path(root_dir, "CarrefourDataEncodingFree.csv")
        formatted_folder_path = os.path.join(root_dir, CONFIG['paths']['formatted_folder'])

        # Create necessary folders
        create_folder(formatted_folder_path)

        # Check if the CSV file exists
        check_file_exists(csv_file_path)

        # Clean the CSV file
        clean_csv(csv_file_path, formatted_folder_path)

    except Exception as e:
        logger.error(f"An error occurred during the CSV cleaning process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
