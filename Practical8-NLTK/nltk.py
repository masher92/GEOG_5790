# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:39:04 2019

@author: gy17m2a
"""
# Import 
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")


# Read in the text from the webpage
url = "http://www.gutenberg.org/files/1321/1321-0.txt"
raw = requests.get(url).text

# Trim text to just the poem based on a starting and ending string
start_pos = raw.rfind("Nam Sibyllam")
end_pos = raw.rfind("Line 415 aetherial] aethereal")
trimmed = raw[start_pos:end_pos]

# Tokenize the raw text
tokens = nltk.word_tokenize(trimmed)
#convert it into a nltk.Text object
text = nltk.Text(tokens)

# Find the 20 most common words
# 
fdist = nltk.FreqDist(text)
print(fdist.most_common(20))





new = ([i for i in tokens if len(i)>1 & len(i)<3])

print([i for i in tokens if i.isalnum() & len(i)>1])
