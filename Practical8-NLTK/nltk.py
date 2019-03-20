import nltk
from nltk.tokenize import RegexpTokenizer
import requests

# Import 
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")


# Read in text of the Wasteland from website.
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
fdist_words = nltk.FreqDist(text)
print(fdist_words.most_common(10))

# Find the 20 most common word lengths
fdist_lengths =  nltk.FreqDist(len(w) for w in text)
print(fdist_lengths.most_common(20))

# Find all the words over 10 letters long
long_words = [wrd for wrd in text if len(wrd) > 10]

# Run part of speech tagging


# Select only tokens that are both alphanumeric and 
tokens_filt = [i for i in tokens if (len(i)>2 and i.isalnum())]

print([i for i in tokens if (len(i)>2 and i.isalnum())])

import re
text = ['this', 'is', 'a', 'sentence', '.']
nonPunct = re.compile('.*[A-Za-z0-9].*')  # must contain a letter or digit
filtered = [w for w in text if nonPunct.match(w)]
