#! python3
"""A program that searches text in your clipboard and returns a list of phone
email addresses
"""

import pyperclip, re

# Create a regex for phone numbers
phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?              # area code
    (\s|-|\.)?                      # seperator
    (\d{3})                         # first 3 digits
    (\s|-|\.)                       # seperator
    (\d{4})                         # last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension
)''', re.VERBOSE)

# Create a regex for email address
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+    #First part of the email
    @                    # @ character
    [a-zA-Z0-9.-]+       # Domain name
    (\.[a-zA-Z]{2,4})    # domain
    (\.[a-zA-Z]{2,4})?   # optional domain
)''', re.VERBOSE)

# Copy text from clipboard
text = str(pyperclip.paste())

matches = []

# Match text from the clipboard
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1],groups[3], groups[5]])
    if groups[8] != '':
        phoneNum += ' x' + groups[8]
    matches.append(phoneNum)

for groups in emailRegex.findall(text):
    matches.append(groups[0])

# Copy the results to the clipboard

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard:')
    print('\n'.join(matches))
else:
    print('No phone numbers or email addresses found')