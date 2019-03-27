## Project 8 - NLTK - Natural Language Toolkit

Natural language processing of the poem "The Wasteland" by T.S.Elliot.  
Intention is to extract proper nouns from the poem and where these correspond to geocodeable places to tag them on a map.  

Current state:
* Poem parsed and split into tokens.
* Various statistics run on the tokens to analyse words appearing in the poem.
* Part of speech tagging performed allowing proper nouns to be extracted
* Many of these proper nouns are not actualy proper nouns - due to the capitilisation which appears in the poem e.g. whole words capitalised or words capitalised on new lines.
* Geocoding of proper nouns not conducted - can't acces Google Geocoding API without supplying bank details.


