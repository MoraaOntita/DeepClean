import os
import pandas as pd

def convert_csv_to_excel(input_file, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Define the output Excel file path
    output_file = os.path.join(output_folder, "final_product_codes.xlsx")
    
    # Save as Excel file
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"File successfully converted and saved at: {output_file}")

if __name__ == "__main__":
    input_csv = "artifacts/cleanshelf/capitalized/capitalized_final_product_codes.csv"
    output_folder = "artifacts/cleanshelf/final_excel"
    
    convert_csv_to_excel(input_csv, output_folder)
