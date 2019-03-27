"""
Natural language processing of the poem "The Wasteland"

Reads in poem from the Gutenburg Project website.
Tokenizes the poem into words.
Computes various statistics on these words and their frequencies.
Identifies proper nouns through part of speech tagging.

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
            
# Remove stop words i.e. common words which don't convey meaning            
# Load stop words
stop_words = stopwords.words('english')
# Remove stop words from tokens
tokens = [word for word in tokens if word not in stop_words]
# Check on which stop words were removed
stop_words_removed = [word for word in tokens if word  in stop_words]

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
# Use ne_chunk

from nltk import pos_tag, ne_chunk
from nltk.tokenize import SpaceTokenizer
sentence = "i spoke with sumit and rajesh and Samit about the gridlock situation last night @ around 8 pm last nite"
tokenizer = SpaceTokenizer()
toks = tokenizer.tokenize(sentence)
pos = pos_tag(toks)
chunked_nes = ne_chunk(pos) 

nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
