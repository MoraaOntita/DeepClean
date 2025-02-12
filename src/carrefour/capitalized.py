import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s: %(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define the BASE_DIR relative to the script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define relative file paths
input_file_path = os.path.join(BASE_DIR, "artifacts", "carrefour", "product_code", "updated_product_codes.csv")
output_folder = os.path.join(BASE_DIR, "artifacts", "carrefour", "capitalized")
output_file_path = os.path.join(output_folder, "capitalized_product_codes.csv")

# Function to capitalize data
def capitalize_data(input_path, output_path):
    try:
        # Load the CSV
        logging.info(f"Loading data from {input_path}")
        df = pd.read_csv(input_path)
        logging.info("Data loaded successfully.")

        # Capitalize all string data in the DataFrame
        logging.info("Capitalizing data...")
        df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
        logging.info("Data capitalized successfully.")

        # Ensure the output folder exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logging.info(f"Directory ensured at: {os.path.dirname(output_path)}")

        # Save the capitalized data
        df.to_csv(output_path, index=False)
        logging.info(f"Capitalized data saved to: {output_path}")
    except Exception as e:
        logging.error(f"An error occurred while capitalizing data: {e}")
        raise

# Run the function
if __name__ == "__main__":
    capitalize_data(input_file_path, output_file_path)
