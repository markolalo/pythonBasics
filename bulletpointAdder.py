#! python3
#bulletPointAdder.py - Adds Wikipedia bullet points to the
#start of each lineof the text on the clipboard

import pyperclip
text = pyperclip.paste()

#Seperate lines and add stars
lines = text.split('\n')
for i in range(len(lines)): #loop through all indexes for "lines" list
    lines[i] = '*'+lines[i] #add star to each string in lines kist

text = '\n'.join(lines) #join the lines
pyperclip.copy(text)