import os
import sys
import pandas as pd
from typing import Callable
from sleeklady import logger
from sleeklady.configurations.config import CONFIG

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
def get_input_file_path() -> str:
    """Return the file path for the input data to be capitalized."""
    return '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/sleeklady/product_code/updated_product_codes.csv'

@log_function_call
def load_csv(file_path: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load CSV file: {file_path} - {str(e)}")
        raise

@log_function_call
def capitalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Capitalize all string data in the DataFrame."""
    # Capitalize the column names
    df.columns = [col.upper() for col in df.columns]
    
    # Capitalize the data in the DataFrame (for string columns)
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].apply(lambda x: str(x).upper() if pd.notna(x) else x)
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
def save_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """Save the DataFrame to a CSV file with explicit encoding."""
    try:
        df.to_csv(file_path, index=False, encoding='utf-8')  # Specify encoding
        logger.info(f"Data saved to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {file_path} - {str(e)}")
        raise


def main():
    """Main function to process the data and capitalize string columns."""
    try:
        # Get the input file path for the data to be capitalized
        input_file_path = get_input_file_path()

        # Load the dataset
        df = load_csv(input_file_path)

        # Capitalize the data in the DataFrame
        df = capitalize_data(df)

        # Resolve the directory path to save the modified file
        capitalized_folder = '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/sleeklady/capitalized'
        create_directory(capitalized_folder)

        # Define the output file path for the capitalized data in the 'capitalized' folder
        output_file_path = os.path.join(capitalized_folder, 'capitalized_data.csv')

        # Save the modified DataFrame to the specified file path
        save_to_csv(df, output_file_path)

    except Exception as e:
        logger.error(f"An error occurred during the process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
