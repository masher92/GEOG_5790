"""
Natural language processing of the poem "The Wasteland"

Reads in poem from the Gutenburg Project website.
Tokenizes the poem into words.
Computes various statistics on these words and their frequencies.
Identifies proper nouns through part of speech tagging.
Filters the proper nouns (due to formatting of poem lots of words are incorrectly identifed as proper nouns) by cutting out stop words and those which are all upper case or include a symbol.

"""

import nltk
import requests
from nltk.corpus import stopwords

# Import extra NLTK packages
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("universal_tagset")
nltk.download('stopwords')

# Read in text of "the Wasteland" from Project Gutenberg website.
url = "http://www.gutenberg.org/files/1321/1321-0.txt"
raw = requests.get(url).text

# Trim text to just the poem, based on a starting and ending string.
start_pos = raw.rfind("Nam Sibyllam")
end_pos = raw.rfind("Line 415 aetherial] aethereal")
trimmed = raw[start_pos:end_pos]

# Tokenize the raw text.
tokens = nltk.word_tokenize(trimmed)

#  Remove tokens which are singular punctuation marks.
for i in tokens:
    if i.isalnum () == False:
        if len (i):
            print (i)
            tokens.remove(i)
            
# Convert tokens into a nltk.Text object.
text = nltk.Text(tokens)

# Find and print the 20 most common words.
fdist_words = nltk.FreqDist(text)
print("The 20 most common words (and their frequencies) are: ", fdist_words.most_common(10))
# Plot a graph of their frequency
#fdist_words.plot(20)

# Find and print the 20 most common word lengths.
fdist_lengths =  nltk.FreqDist(len(w) for w in text)
print("The 20 most common word lengths (and their frequencies)  are: ", fdist_lengths.most_common(20))

# Find all the words over 10 letters long.
long_words = [wrd for wrd in text if len(wrd) > 10]
print("The following words are over 10 letters long: " + ', '.join(long_words))

# Run part of speech tagging
# If tagset is set to 'universal', then words split into higher level groups e.g. nouns rather than proper nouns. 
#tagged = nltk.pos_tag(text, tagset='universal')
tagged = nltk.pos_tag(text)

# Find the frequency of the proper nouns
freq = nltk.FreqDist(tagged)
proper_noun_freq = [(tag_pair[0], fre) for (tag_pair, fre) in 
					freq.most_common() if tag_pair[1] == 'NNP']

# Create a list containing just the proper nouns
proper_nouns = []
for tag in tagged:
    if tag[1] == "NNP":
            print (tag[0])
            proper_nouns.append(tag[0])

# Filter out some of the dubious proper nouns
# Remove those words which are all upper case or which contain a symbol.
uppercase = []
symbols = []
for noun in proper_nouns:
    if noun.isupper() == True:
        uppercase.append(noun)
        # Remove value from proper nouns list
        proper_nouns = list(filter(lambda a: a != noun, proper_nouns))
    if noun.isalpha() == False:
        symbols.append(noun)
        # Remove value from proper nouns list
        proper_nouns = list(filter(lambda a: a != noun, proper_nouns))

# Remove stop words i.e. common words which don't convey meaning            
# Load stop words
stop_words = stopwords.words('english')
# Convert all the words
print ("The following stop words have been removed:")
cleaned_pn = []
for noun in proper_nouns:
   # print(noun.lower())
    if noun.lower() not in stop_words:
        cleaned_pn.append(noun)
    else:
        print(noun)

# Named entity tagging to get locations?
# Geocoding check https://developer.here.com/blog/turn-text-into-here-maps-with-python-nltk
