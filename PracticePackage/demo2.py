import argparse

parser = argparse.ArgumentParser()
parser.add_argument('str', help='Enter Your String: ')
args = parser.parse_args()
print(args.str)

