import json, string, nltk, random, pickle
from nltk.classify import NaiveBayesClassifier
from features import *

def train_model(train_features):
	classifier = NaiveBayesClassifier.train(train_features)
	return classifier

def main(data_train):
	featureset = []
	random.shuffle(data_train)

	#data_train is the manually annotated data which will be used for training and testing
	for data in data_train:
		for review, sentiment in data.iteritems():

			#stopwords removal, stemming :preProcess the text
			words = preProcess(review)
			featureset.append((word_feats(words), sentiment))

	split_at = int(len(featureset)*0.80)
	print "Training for " + str(split_at) + " and validating for " + str(len(featureset) - split_at) 

	train_set, validation_set = featureset[:split_at], featureset[split_at:]
	classifier = train_model(train_set)
	print "Validation set accuracy : " + str(nltk.classify.accuracy(classifier, validation_set)*100) + "%"
	return classifier

if __name__ == "__main__":
	data_train = json.loads(open('../../DATA/sentiment/data_train.json').read())
	classifier = main(data_train)

	#dump the classifier
	f = open('classifier.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()
