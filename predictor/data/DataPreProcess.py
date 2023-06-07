import string
import re
import argparse
from sklearn.model_selection import train_test_split

# Create the parser
parser = argparse.ArgumentParser(description="Clean and split text data")

# Add the arguments
parser.add_argument('--file', '-f', type=str, help="The name of the data file")
parser.add_argument('--train', '-tr', type=str, help="The name of the train data file")
parser.add_argument('--test', '-t', type=str, help="The name of the test data file")

# Parse the arguments
args = parser.parse_args()

# Read the data from the file
with open(args.file, 'r') as file:
    data = file.read()

# Split data into paragraphs
paragraphs = data.split('\n')

# Clean each paragraph
for i in range(len(paragraphs)):
    # Remove anything that isn't a space, an apostrophe, or a letter
    paragraphs[i] = re.sub(r"[^a-zA-Z' ]+", '', paragraphs[i])
    # Replace extra whitespace
    paragraphs[i] = re.sub(r'\s+', ' ', paragraphs[i]).strip()

# Split the paragraphs into training and testing data
train_data, test_data = train_test_split(paragraphs, test_size=0.1, random_state=42)

# Write the training data to a file
with open(args.train, 'w') as file:
    for paragraph in train_data:
        file.write(paragraph + ' ')

# Write the training data for NN
with open("nn_"+args.train, 'w') as file:
    for paragraph in train_data:
        file.write(paragraph + '\n')


with open("shortened_"+args.train, 'w') as file:
    nb_lines = 0
    for paragraph in train_data:
        file.write(paragraph + '\n')
        nb_lines += 1
        if nb_lines >= 300000:
            break
# Write the testing data to a file
with open(args.test, 'w') as file:
    for paragraph in test_data:
        file.write(paragraph + '\n')

# Shortened version
with open("shortened_"+args.test, 'w') as file:
    nb_lines = 0
    for paragraph in test_data:
        file.write(paragraph + '\n')
        nb_lines += 1
        if nb_lines >= 1000:
            break
