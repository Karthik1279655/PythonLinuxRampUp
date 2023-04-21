import re

# Define the regular expression pattern
pattern = r'\b\w{4}\b'

# Define the string to search for matches
string = 'The quick brown fox jumps over the lazy dog'

# Use the re.findall method to find all matches of the pattern in the string
matches = re.findall(pattern, string)

# Print the matches
print(id(matches), flush=True)
print(id(matches))

