import pandas as pd
import os

# Define the path to the Excel file
excel_file = '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/Data/Cleanshelf/Cleanshelf Sellout Data ALKHEMY BRANDS OCT.xlsx'

# Define the directory where the CSV should be saved
output_dir = '/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/artifacts/cleanshelf'

# Ensure the directory exists, create if not
os.makedirs(output_dir, exist_ok=True)

# Read the Excel file
df = pd.read_excel(excel_file)

# Define the CSV file path
csv_file = os.path.join(output_dir, 'formatted_data.csv')

# Save the data to CSV
df.to_csv(csv_file, index=False)

print(f"File converted to CSV and saved as: {csv_file}")
