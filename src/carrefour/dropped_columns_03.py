import os
import sys
import pandas as pd
from typing import List

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
def get_csv_file_path(file_name: str) -> str:
    """Get the full path of the CSV file."""
    return os.path.join(CONFIG['paths']['filtered_folder'], file_name)


@log_function_call
def read_csv_file(file_path: str) -> pd.DataFrame:
    """Read the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to read CSV file: {file_path} - {str(e)}")
        raise


@log_function_call
def drop_columns(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Drop specified columns from the DataFrame."""
    try:
        return data.drop(columns=columns, axis=1)
    except Exception as e:
        logger.error(f"Failed to drop columns: {str(e)}")
        raise


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
def save_dropped_columns_data(data: pd.DataFrame, file_path: str) -> None:
    """Save the data with dropped columns to a CSV file."""
    try:
        data.to_csv(file_path, index=False)
        logger.info(f"Data with dropped columns saved as CSV: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save dropped columns data to CSV: {str(e)}")
        raise


def main():
    """Main function to execute the drop columns process."""
    try:
        # Get the file path for the filtered CSV file
        csv_file_path = get_csv_file_path('alkhemy_brands_data.csv')

        # Read the CSV file into a DataFrame
        data = read_csv_file(csv_file_path)

        # Drop the specified columns
        columns_to_drop = ['Year', 'Month', 'Dept', 'Dept Name', 'Section', 'Section Name', 'Family', 'Family name', 'Sub Family', 
                           'Sub Family Name', 'Brand No', 'Brand Principle', 'Brand Name', 'SupplierNo', 'Item Code', 'Item Bar Code',
                           'Unnamed: 31', 'Unnamed: 32', 'Unnamed: 48', 'Unnamed: 49', 'MKT Code', 'MKT Name', 'SupplierName']
        

        data_dropped = drop_columns(data, columns_to_drop)

        # Get the folder path for saving the dropped columns data
        dropped_columns_folder_path = CONFIG['paths']['dropped_folder']
        create_folder(dropped_columns_folder_path)

        # Define the file path for the CSV file with dropped columns
        dropped_columns_csv_file_path = os.path.join(dropped_columns_folder_path, 'alkhemy_brands_dropped_columns.csv')

        # Save the data with dropped columns to a new CSV file
        save_dropped_columns_data(data_dropped, dropped_columns_csv_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the drop columns process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
