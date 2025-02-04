import os
import pandas as pd
import yaml
import sys

# Load configurations from config.yaml
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'configuration', 'config.yaml')
    print("Config file path:", config_path)  # Debugging line to print the file path
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

# Import config.py directly (this file contains Python code)
def load_python_config():
    config_path = os.path.join(os.path.dirname(__file__), 'configuration', 'config.py')
    print("Python config file path:", config_path)  # Debugging line to print the file path
    
    # Add the folder to sys.path so we can import config.py as a module
    sys.path.append(os.path.dirname(config_path))
    
    # Import config.py
    import config
    
    # Return the necessary configurations from config.py (e.g., CONFIG and PRODUCT_CODES)
    return config

# Main function to change file format
def process_file():
    # Load configurations
    config = load_config()  # YAML config
    python_config = load_python_config()  # Python config

    # Use the values loaded from the YAML file
    input_file_path = config['file_paths']['input_file']
    output_file_path = config['file_paths']['output_file']

    # Read Excel file
    df = pd.read_excel(input_file_path, header=None)

    # Delete the first 8 rows
    df = df.iloc[8:].reset_index(drop=True)

    # Save to CSV
    df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    process_file()
