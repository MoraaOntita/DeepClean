import pandas as pd

# Load the dataset
file_path = 'artifacts/cleanshelf/formatted/cleaned_data.csv'
data = pd.read_csv(file_path)

# Filter the data for suppliers from ALKHEMY BRANDS LIMITED
filtered_data = data[data['Supp_Name'] == 'ALKHEMY BRANDS LIMITED']

# Save the filtered data
output_path = 'artifacts/cleanshelf/filtered/filtered_data.csv'
filtered_data.to_csv(output_path, index=False)

print(f"Filtered data saved to: {output_path}")
