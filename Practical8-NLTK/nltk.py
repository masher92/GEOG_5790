import nltk
from nltk.tokenize import RegexpTokenizer
import requests
import re

# Import extra NLTK packages
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("universal_tagset")

"""
Natural language processing of the poem "The Wasteland"

Reads in poem from the Gutenburg Project website.
Tokenizes the poem into words and identifies proper nouns through part of speech tagging.


"""

# Read in text of "the Wasteland" from website.
url = "http://www.gutenberg.org/files/1321/1321-0.txt"
raw = requests.get(url).text

# Trim text to just the poem based on a starting and ending string
start_pos = raw.rfind("Nam Sibyllam")
end_pos = raw.rfind("Line 415 aetherial] aethereal")
trimmed = raw[start_pos:end_pos]

# Tokenize the raw text
tokens = nltk.word_tokenize(trimmed)

#  Remove tokens whichare singular punctuation marks
for i in tokens:
    if i.isalnum () == False:
        if len (i) ==1 or len(i) == 2 :
            print (i)
            tokens.remove(i)


#convert it into a nltk.Text object
text = nltk.Text(tokens)

# Find the 20 most common words
fdist_words = nltk.FreqDist(text)
print(fdist_words.most_common(10))
fdist_words.plot(20)

# Find the 20 most common word lengths
fdist_lengths =  nltk.FreqDist(len(w) for w in text)
print(fdist_lengths.most_common(20))

# Find all the words over 10 letters long
long_words = [wrd for wrd in text if len(wrd) > 10]

# Run part of speech tagging
#tagged = nltk.pos_tag(text, tagset='universal')
tagged = nltk.pos_tag(text)

# NNPs
# Finds the frequency of the proper nouns
freq = nltk.FreqDist(tagged)
proper_noun_freq = [(tag_pair[0], fre) for (tag_pair, fre) in 
					freq.most_common() if tag_pair[1] == 'NNP']

# Create a list containing just the proper nouns
proper_nouns = []
for tag in tagged:
    if tag[1] == "NNP":
            print (tag)
            proper_nouns.append(tag)
# Other method
propernouns2 = [tag for tag,pos in tagged if pos == 'NNP']

# Filter out some of the dubious proper nouns
            

