import re, collections
import json
from nltk.corpus import stopwords

test_data = json.loads(open('test.json').read())
golden_data = json.loads(open('golden.json').read())

count = 0
avg_recall = 0.0
for tdata in test_data:
	for gdata in golden_data:
		if tdata['title'] != gdata['title']:
			continue
		count += 1
		test_features = tdata['splitkeys']
		golden_features = gdata['splitkeys']
		overlap = list(set(test_features)&set(golden_features))
		activity_recall = float(len(overlap))/float(len(golden_features))
		avg_recall += activity_recall
		print "Activity " + str(count) + " Recall: " + str(activity_recall)

print "Average Recall: " + str(avg_recall/count)
