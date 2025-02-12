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
def get_excel_file_path(root_dir: str, file_name: str) -> str:
    """Resolve the path to the Excel file."""
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
        logger.error(f"Excel file not found at: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")


@log_function_call
def read_excel_file(file_path: str) -> Dict[str, pd.DataFrame]:
    """Read the Excel file and return all sheets as DataFrames."""
    try:
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        logger.error(f"Failed to read Excel file: {file_path} - {str(e)}")
        raise


@log_function_call
def convert_to_csv(data: pd.DataFrame, sheet_name: str, folder_path: str) -> str:
    """Convert an Excel sheet to CSV without modifying rows."""
    try:
        csv_file_path = os.path.join(folder_path, f"{sheet_name}_raw.csv")
        data.to_csv(csv_file_path, index=False)  # Save raw CSV first
        logger.info(f"Converted {sheet_name} to CSV: {csv_file_path}")
        return csv_file_path
    except Exception as e:
        logger.error(f"Failed to convert {sheet_name} to CSV: {str(e)}")
        raise


@log_function_call
def clean_csv(csv_file_path: str, sheet_name: str, folder_path: str) -> None:
    """Remove the first six rows from the CSV file and save the cleaned version."""
    try:
        # Load the CSV without headers
        df = pd.read_csv(csv_file_path, header=None)

        # Ensure there are enough rows to remove
        if df.shape[0] > 6:
            df = df.iloc[6:].reset_index(drop=True)  # Drop first 6 rows
            df.columns = df.iloc[0]  # Set the new header from row 7
            df = df[1:].reset_index(drop=True)  # Drop the new header row from data

        cleaned_csv_path = os.path.join(folder_path, f"{sheet_name}.csv")
        df.to_csv(cleaned_csv_path, index=False)
        
        logger.info(f"Cleaned CSV saved: {cleaned_csv_path}")

    except Exception as e:
        logger.error(f"Failed to clean CSV {csv_file_path}: {str(e)}")
        raise


def main():
    """Main function to execute the format change pipeline."""
    try:
        excel_file_path = get_excel_file_path(root_dir, "KE-23-0229-CGD-ALKH-Y24-M12-12.xlsx")
        formatted_folder_path = os.path.join(root_dir, CONFIG['paths']['formatted_folder'])

        # Create necessary folders
        create_folder(formatted_folder_path)

        # Check if the Excel file exists
        check_file_exists(excel_file_path)

        # Read the Excel file
        excel_data = read_excel_file(excel_file_path)

        # Process each sheet: Convert to CSV, delete rows, and save cleaned version
        for sheet_name, data in excel_data.items():
            csv_file_path = convert_to_csv(data, sheet_name, formatted_folder_path)
            clean_csv(csv_file_path, sheet_name, formatted_folder_path)

    except Exception as e:
        logger.error(f"An error occurred during the format change process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
