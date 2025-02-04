import os
import sys
import pandas as pd
from typing import Callable

# Add the src folder to sys.path to ensure it can find sleeklady
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
def get_input_csv_path() -> str:
    """Resolve the input CSV file path from the configuration."""
    return os.path.join(CONFIG['paths']['capitalized_folder'], CONFIG['files']['input_capitalized_csv'])


@log_function_call
def load_csv(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {str(e)}")
        raise


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
def save_to_excel(df: pd.DataFrame, file_path: str) -> None:
    """Save the DataFrame to an Excel file."""
    try:
        df.to_excel(file_path, index=False)
        logger.info(f"Excel file saved to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save Excel file: {file_path} - {str(e)}")
        raise


def main():
    """Main function to transform the data and save it as an Excel file."""
    try:
        # Get the input CSV file path
        input_csv_path = get_input_csv_path()

        # Load the dataset
        df = load_csv(input_csv_path)

        # Resolve the output directory path for Excel files
        output_dir = CONFIG['paths']['final_excel_folder']
        create_directory(output_dir)

        # Define the output Excel file path
        output_excel_path = os.path.join(output_dir, CONFIG['files']['output_excel_filename'])

        # Save the DataFrame to the output Excel file
        save_to_excel(df, output_excel_path)

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
