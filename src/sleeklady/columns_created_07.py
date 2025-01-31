import os
import sys
import pandas as pd
from sleeklady.configurations.config import CONFIG
from typing import Callable
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
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns as needed."""
    df.rename(columns={'TotalSellingPrice': 'Total Sales'}, inplace=True)
    return df


@log_function_call
def add_new_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add new columns and fill them with the required values."""
    df['Account Name'] = 'SLEEK LADY'
    df['Group'] = 'MT'
    df['Sales Rep'] = 'Leah'
    df['Date'] = 'DEC24'
    return df


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
    """Main function to process the CSV and add new columns."""
    try:
        # Define the file paths from the configuration
        input_file_path = os.path.join(CONFIG['paths']['store_folder'], 'modified_with_resolved_store_names.csv')
        output_folder = CONFIG['paths']['columns_created']
        
        # Create the output directory if it doesn't exist
        create_directory(output_folder)

        # Load the CSV file
        df = load_csv(input_file_path)

        # Rename columns
        df = rename_columns(df)

        # Add new columns
        df = add_new_columns(df)

        # Define the output file path
        output_file_path = os.path.join(output_folder, 'columns_added.csv')

        # Save the updated DataFrame to the new folder
        save_to_csv(df, output_file_path)

        print(f"Columns added successfully and saved to {output_file_path}")

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
