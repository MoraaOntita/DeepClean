import os
import sys
import pandas as pd
import re
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
def classify_product(product_name: str) -> str:
    """Classify products based on regex patterns."""
    product_name = product_name.lower()

    # Fetch patterns from the configuration
    patterns = CONFIG['product_classification_patterns']

    # Check each category using regex
    for category, pattern in patterns.items():
        if re.search(pattern, product_name):
            return category

    return 'Unclassified'  # Default if no match


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
    """Main function to process the CSV and classify products."""
    try:
        # Get the full path of the CSV file from config
        file_path = get_file_path(CONFIG['files']['brands_csv'])

        # Load the dataset
        df = load_csv(file_path)

        # Drop 'Categories' column if it exists
        if 'Categories' in df.columns:
            df = df.drop(columns=['Categories'])

        # Create and classify the 'Categories' column
        df['Categories'] = df['ProductDescriptions'].apply(classify_product)

        # Resolve the output folder path from the configuration
        output_folder = CONFIG['paths']['categories_folder']
        create_directory(output_folder)

        # Define the output file path for saving the modified dataset from config
        output_file_path = os.path.join(output_folder, CONFIG['files']['modified_csv'])

        # Save the updated dataset to the specified file path
        save_to_csv(df, output_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
