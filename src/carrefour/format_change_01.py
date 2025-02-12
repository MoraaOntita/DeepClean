import os
import sys
import pandas as pd
import logging
from typing import Dict, Optional


# Add the project root directory to sys.path
#root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#sys.path.append(root_dir)

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
    """Read the Excel file and return all sheets."""
    try:
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        logger.error(f"Failed to read Excel file: {file_path} - {str(e)}")
        raise


@log_function_call
def save_and_reload_csv(data: pd.DataFrame, sheet_name: str, folder_path: str) -> pd.DataFrame:
    """Remove first five rows, save as CSV, and reload the CSV while keeping correct headers."""
    try:
        if data.shape[0] > 5:
            data = data.iloc[5:]  # Drop first 5 rows
            data.reset_index(drop=True, inplace=True)  # Reset index

        csv_file_path = os.path.join(folder_path, f"{sheet_name}.csv")
        data.to_csv(csv_file_path, index=False)

        # Reload CSV and explicitly set headers
        reloaded_data = pd.read_csv(csv_file_path, header=0)
        
        logger.info(f"Saved {sheet_name} as CSV after removing first five rows: {csv_file_path}")
        logger.info(f"Reloaded CSV: {csv_file_path}")

        return reloaded_data

    except Exception as e:
        logger.error(f"Failed to process {sheet_name}: {str(e)}")
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

        # Process each sheet: delete rows, save as CSV, and reload CSV
        for sheet_name, data in excel_data.items():
            reloaded_data = save_and_reload_csv(data, sheet_name, formatted_folder_path)

            # You can now use `reloaded_data` for further processing if needed
            print(f"Reloaded CSV for {sheet_name}:\n", reloaded_data.head())

    except Exception as e:
        logger.error(f"An error occurred during the format change process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
