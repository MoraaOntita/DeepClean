import pandas as pd
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def drop_columns_and_save(input_file):
    """Drop specific columns and save the result in the 'dropped' folder."""
    
    # Load the transformed dataset
    df = pd.read_csv(input_file)
    
    # Columns to drop
    columns_to_drop = ['ITEMLOOKUPCODE', 'BARCODE', 'CATEGORY']
    
    # Drop the specified columns
    df = df.drop(columns=columns_to_drop, errors='ignore')  # 'ignore' ensures it doesn't break if a column is missing
    
    # Define output directory and create it if it doesn't exist
    output_dir = 'artifacts/naivas/dropped'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the modified file
    output_path = os.path.join(output_dir, 'cleaned_data_final.csv')
    df.to_csv(output_path, index=False)
    
    logging.info(f"Columns dropped and data saved to {output_path}")

# Example usage
input_file = 'artifacts/naivas/edited_columns/cleaned_data_transformed.csv'
drop_columns_and_save(input_file)
