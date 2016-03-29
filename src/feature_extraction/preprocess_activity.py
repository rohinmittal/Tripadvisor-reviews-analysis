import json, nltk
from stopwords import *
import string, unidecode

def preprocess_activity(activity):
        phrases = activity['Keywords']
        #phrases = activity['reviews']
	split_keys = split_phrases(phrases)
	activity['splitkeys'] = split_keys

def split_phrases(phrases):
	split_phrases = []
	for phrase in phrases:
		phrase = unidecode.unidecode(phrase)
		phrase = phrase.translate(None, string.punctuation)
		keywords = phrase.split()
		for word in keywords:
			#lower case
			word = word.lower()
			#remove stop words
			if word in stopwords:
				continue
			#stem words
			stemmed_word = nltk.stem.porter.PorterStemmer().stem(word)
			split_phrases.append(stemmed_word)

	return split_phrases
