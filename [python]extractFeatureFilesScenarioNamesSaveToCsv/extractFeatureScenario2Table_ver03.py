import os
import re
import csv
import sys
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Ex: python3 extractFeatureScenario2Table.py <folderNameContainsFeatureFiles>')

# Parse the command line arguments
args = parser.parse_args()

# Read the value of the HOME environment variable
home_dir = os.environ['HOME']

# The fixed string
prefix = '/work/elisa2/test/ui/squish/EPC/'

# The input parameter (the name of a folder)
# Read the first command line argument
folder_name = sys.argv[1]

# Concatenate the strings
directory = home_dir + prefix + folder_name

# Regex pattern to match the desired information in the feature files
pattern = r'(?:Scenario\:\s+[\s\S]*?(?=\n)|Scenario Outline\:\s+[\s\S]*?(?=\n))'

# Create empty lists to store file names and information
feature_files = []
information = []

# Use os.walk to iterate over all files and directories in the specified directory
for root, dirs, files in os.walk(directory):
    # Iterate over the files in the current directory
    for file in files:
        # Check if the file name ends with ".feature" and store the file name if it does
        if file.endswith(".feature"):
            feature_files.append(file)

# Write the list of feature files to a CSV file called "feature.csv"
with open("featureList.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    for file in feature_files:
        writer.writerow([file])

# Iterate over the feature files and extract information that matches a regular expression
for file in feature_files:
    with open(file, "r") as f:
        # Read the contents of the file
        contents = f.read()

        # Use a regular expression to extract the desired information
        matches = re.findall(pattern, contents)

        # Append the extracted information to the list of information
        information.extend(matches)

# Write the list of information to a CSV file called "information.csv"
with open("scenarioList.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    for info in information:
        writer.writerow([info])
        
# Open a CSV file for writing the results
with open('tempOut.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)

  # Write the header row
  writer.writerow(['Feature file', 'Scenario name'])

  # Iterate over all the feature files
  for feature_file in os.listdir(directory):
    if feature_file.endswith('.feature'):  # only process .feature files
      with open(os.path.join(directory, feature_file)) as f:
        # Read the entire file as a string
        feature_str = f.read()
        # Use the regex pattern to find all matches in the file
        matchesInfo = re.findall(pattern, feature_str)
        # Write each match to the CSV file
        for match in matchesInfo:
          writer.writerow([feature_file, match])
   
# Open the input CSV file for reading
with open('tempOut.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)

  # Read the header row
  header = next(reader)

  # Sort the rows by the first column (assumed to be the name of the feature file)
  sorted_rows = sorted(reader, key=lambda x: x[0])

  # Open the output CSV file for writing
  with open('outputFeatureScenario.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Write the header row
    writer.writerow(header)

    # Write the sorted rows
    for row in sorted_rows:
      writer.writerow(row)
    
# The names of the CSV files to remove
csv_files = ['tempOut.csv', 'scenarioList.csv', 'featureList.csv']

# Iterate over the list of CSV files
for csv_file in csv_files:
  # Construct the full path to the CSV file
  file_path = os.path.join(directory, csv_file)

  try:
    # Attempt to remove the file
    os.remove(file_path)
  except FileNotFoundError:
    # Handle the case where the file doesn't exist
    print(f'{file_path} does not exist')
  except PermissionError:
    # Handle the case where you don't have permission to delete the file
    print(f'You do not have permission to delete {file_path}')   
        
