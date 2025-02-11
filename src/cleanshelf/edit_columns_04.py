import pandas as pd
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def transform_data(file_path):
    """Transform the dataset into long format with correct Sold Qty and Value alignment."""
    # Load the data
    df = pd.read_csv(file_path)
    
    # Define the store columns for Sold Qty and Value (both for Sold Qty and Value)
    store_columns = [
        'COVO-LAVINGTON', 'FRESHMARKET', 'GREEN PARK', 'KAHAWA WEST', 'KERUGOYA', 'KIAMBU', 'KIKUYU',
        'K-MALL', 'LANGATA', 'LIMURU', 'NAKURU', 'NGONG', 'NYAHURURU', 'RONGAI', 'RUAKA', 'SOUTH B', 'WENDANI'
    ]
    
    # Create a list to hold all the transformed rows
    transformed_data = []

    # Iterate over each row in the original dataframe
    for _, row in df.iterrows():
        product_code = row['Product_Code']
        product_desc = row['Product_Desc']
        dept_name = row['Dept_Name']
        class_name = row['Class_Name']
        supp_name = row['Supp_Name']

        # Loop through each store and gather the corresponding Sold Qty and Value
        for store in store_columns:
            sold_qty_col = f'{store}_Sold Qty'
            value_col = f'{store}_Value'
            
            sold_qty = row[sold_qty_col]
            value = row[value_col]

            # Only add a row if there was a valid sold quantity
            if pd.notna(sold_qty) and sold_qty > 0:
                transformed_data.append({
                    'Product_Code': product_code,
                    'Product_Desc': product_desc,
                    'Dept_Name': dept_name,
                    'Class_Name': class_name,
                    'Supp_Name': supp_name,
                    'StoreName': store,
                    'Sold Qty': sold_qty,
                    'Value': value
                })

    # Create a new DataFrame from the transformed data
    transformed_df = pd.DataFrame(transformed_data)

    # Define the output path
    output_dir = 'artifacts/cleanshelf/edited_columns'
    # Create the directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the transformed data
    output_path = os.path.join(output_dir, 'cleaned_data_transformed.csv')
    transformed_df.to_csv(output_path, index=False)
    logging.info(f"Data transformation completed and saved to {output_path}")

# Example usage
file_path = 'artifacts/cleanshelf/filtered/filtered_data.csv'
transform_data(file_path)
