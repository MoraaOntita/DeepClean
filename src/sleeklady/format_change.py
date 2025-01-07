import pandas as pd
import os

# Define the file path of the Excel file
excel_file_path = '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/Data/Bestlady Alkhemy November 2024 data.xlsx'

# Define the artifacts/formated folder path
formatted_folder_path = '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/formated'

# Create the formatted folder if it doesn't exist
os.makedirs(formatted_folder_path, exist_ok=True)

# Read the Excel file
excel_data = pd.read_excel(excel_file_path, sheet_name=None)  # sheet_name=None to load all sheets

# Optionally, check sheet names
print("Sheet names:", excel_data.keys())

# Convert each sheet to a separate CSV file in the formatted folder
for sheet_name, data in excel_data.items():
    csv_file_path = os.path.join(formatted_folder_path, f'{sheet_name}.csv')
    data.to_csv(csv_file_path, index=False)  # Save to CSV, without row indices
    print(f"Saved {sheet_name} as CSV: {csv_file_path}")
