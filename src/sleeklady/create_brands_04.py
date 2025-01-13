import os
import sys
import pandas as pd
from typing import Any
from sleeklady import logger
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
def get_file_path(file_name: str) -> str:
    """Resolve the full path for a CSV file from the configuration."""
    return os.path.join(CONFIG['paths']['dropped_folder'], file_name)


@log_function_call
def load_csv(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {str(e)}")
        raise


@log_function_call
def create_brands_column(df: pd.DataFrame) -> pd.DataFrame:
    """Create a new 'Brands' column based on the 'ProductDescriptions'."""
    try:
        df['Brands'] = df['ProductDescriptions'].apply(
            lambda x: 'Mikalla' if str(x).startswith('MIKALLA')
                      else 'H&B' if str(x).startswith('H&B')
                      else 'Unknown'
        )
        return df
    except Exception as e:
        logger.error(f"Failed to create 'Brands' column: {str(e)}")
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
def save_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """Save the DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        logger.info(f"Data saved to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {file_path} - {str(e)}")
        raise


def main():
    """Main function to process the CSV and create the Brands column."""
    try:
        # Get the full path of the CSV file
        file_path = get_file_path('alkhemy_brands_dropped_columns.csv')

        # Load the dataset
        df = load_csv(file_path)

        # Create the 'Brands' column
        df = create_brands_column(df)

        # Resolve the output folder path from the configuration
        output_folder = CONFIG['paths']['brands_folder']
        create_directory(output_folder)

        # Define the output file path for saving the updated dataset
        output_file_path = os.path.join(output_folder, 'alkhemy_brands_with_brands_column.csv')

        # Save the updated dataset to the specified file path
        save_to_csv(df, output_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
