import pandas as pd

# Load the data (replace 'file.xlsx' with your actual file path)
data = pd.read_excel('/home/moraa-ontita/Documents/Machine-learning/DeepCleanAI/Data/Cleanshelf/Cosmetics december 2024 sales data.xlsx')  # or pd.read_csv('file.csv')

# Reshape the data to have one column for "Location" and another for "Type" and "Value"
reshaped_data = pd.melt(data, 
                        id_vars=[], 
                        var_name="Location", 
                        value_name="Details")

# Save the reshaped data
reshaped_data.to_csv('reshaped_data.csv', index=False)
print("Data reshaped successfully!")
