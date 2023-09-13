import pandas as pd
from bs4 import BeautifulSoup
import uuid
import json

# Replace 'your_input.html' with the path to your HTML file
html_file = 'S:\Autoradio\FM\Frequenties.html'

# Parse the HTML file using BeautifulSoup
with open(html_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find the table in the HTML (adjust 'table_id' as needed)
table = soup.find('table', id='tablepress-51')

# Create an empty list to store the JSON objects
json_data = []

# Create a dictionary to keep track of names and corresponding data
name_data_dict = {}

# Function to format the number as described
def format_number(number):
    return str(int(float(number) * 100))

# Iterate through the rows of the table
for row in table.find_all('tr'):
    columns = row.find_all('td')
    
    if len(columns) >= 2:
        name = columns[1].get_text(strip=True)
        value = columns[0].get_text(strip=True)
        
        if name in name_data_dict:
            # Check if the value is not already in the freqlist
            if format_number(value) not in name_data_dict[name]['freqlist']:
                name_data_dict[name]['freqlist'].append(format_number(value))
        else:
            name_data_dict[name] = {
                "sid": 0,
                "uuid": str(uuid.uuid4()),
                "name": name,
                "freq": format_number(value),  # Format the number
                "freqRangeId": 0,
                "favorite": False,
                "freqlist": [format_number(value)]  # Add the formatted value to the freqlist initially
            }

# Extract JSON objects from the collected data
for name, data in name_data_dict.items():
    json_data.append(data)

# Save the JSON data to a file (replace 'output.json' with your desired output file name)
output_file = 'S:\Autoradio\FM\RadioListNL3.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Conversion complete. JSON saved to {output_file}")
