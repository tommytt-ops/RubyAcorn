import re
import csv
import pandas as pd


# Define regular expression patterns for each field
patterns = {
    'title': r'title="([^"]+)"',
    'type': r'type="([^"]*)"',
    'releasedate': r'releasedate="([^"]*)"',
    'developer': r'developer="([^"]*)"',
    'publisher': r'publisher="([^"]*)"',
    'category': r'category="([^"]*)"',


}

# Initialize a list to store the extracted data
extracted_data = []

# Create a list of field names in the correct order
field_names = list(patterns.keys())

# Create a set to keep track of unique titles
unique_titles = set()

# Read data from the text file and process each line
with open('./prominfo.txt', 'r') as file:
    for line in file:
        # Initialize data_row for each line
        data_row = {field: "" for field in field_names}

        # Iterate through the patterns and extract data
        for field, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                data_row[field] = match.group(1)

        # Check if the title is unique before appending to extracted_data
        title = data_row['title']
        extracted_data.append([data_row[field] for field in field_names])
        unique_titles.add(title)

# Save the extracted data to a CSV file
with open('labels_and_data.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row with field names
    csv_writer.writerow(field_names)

    # Write data rows with corresponding values
    csv_writer.writerows(extracted_data)


