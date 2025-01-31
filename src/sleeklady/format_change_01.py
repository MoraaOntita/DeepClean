import os
import sys
import pandas as pd
import logging
from typing import Dict

# Import the custom logger
from sleeklady import logger

# Add the project root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from sleeklady.configurations.config import CONFIG


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
def get_excel_file_path() -> str:
    """Resolve the path to the Excel file dynamically."""
    return os.path.join(CONFIG['paths']['data_folder'], CONFIG['files']['input_excel'])


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
        logger.error(f"Excel file not found at: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")


@log_function_call
def read_excel_file(file_path: str) -> Dict[str, pd.DataFrame]:
    """Read the Excel file and return all sheets."""
    try:
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        logger.error(f"Failed to read Excel file: {file_path} - {str(e)}")
        raise


@log_function_call
def save_sheet_as_csv(data: pd.DataFrame, sheet_name: str, folder_path: str) -> None:
    """Save a DataFrame as a CSV file."""
    try:
        csv_file_path = os.path.join(folder_path, f"{sheet_name}.csv")
        data.to_csv(csv_file_path, index=False)
        logger.info(f"Saved {sheet_name} as CSV: {csv_file_path}")
    except Exception as e:
        logger.error(f"Failed to save {sheet_name} as CSV: {str(e)}")
        raise


def main():
    """Main function to execute the format change pipeline."""
    try:
        # Get file paths dynamically
        excel_file_path = get_excel_file_path()
        formatted_folder_path = CONFIG['paths']['formatted_folder']

        # Create necessary folders
        create_folder(formatted_folder_path)

        # Check if the Excel file exists
        check_file_exists(excel_file_path)

        # Read the Excel file
        excel_data = read_excel_file(excel_file_path)

        # Convert each sheet to a separate CSV file
        for sheet_name, data in excel_data.items():
            save_sheet_as_csv(data, sheet_name, formatted_folder_path)

    except Exception as e:
        logger.error(f"An error occurred during the format change process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
