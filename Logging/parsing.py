import argparse
import logging

parser = argparse.ArgumentParser(description='Process some integers.')

# Add a command-line option
parser.add_argument('--input', dest='input_file1', help='input file name')

# Parse the command-line arguments
args = parser.parse_args()

# Open the input file for reading and the output file for writing
try:
    with open('report.txt', 'r') as input_file, open("output_file1.txt", "w") as output_file:
        # Loop through each line in the input file
        for line in input_file:
            # Check if the string is present in the line
            if args.input_file1 in line:
                # If it is, write the line to the output file
                output_file.write(line)

# if input file not present throw an exception
except Exception as e:
    logging.error(str(e))

