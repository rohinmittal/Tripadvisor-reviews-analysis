import pickle, json, sys
from features import * 

def detect(classifier, review):
	words = preProcess(review)
	return classifier.classify(word_feats(words))

def test(classifier, data_test):

	match = 0
	print "Testing for : " + str(len(data_test)) + " reviews."
	for data in data_test:
		for review, sentiment in data.iteritems():
			detectedSentiment = detect(classifier, review)
			if detectedSentiment == sentiment:
				match = match + 1
	
	print "Sentiment match : " + str(match) + "/" + str(len(data_test))


if __name__ == '__main__':
	f = open('classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()

	if len(sys.argv) == 1:
		data_test = json.loads(open('../../DATA/sentiment/data_test.json').read())
		test(classifier, data_test)
	else:
		print detect(classifier, sys.argv[1])

