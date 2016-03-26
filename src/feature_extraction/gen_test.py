import json, numpy, operator
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess_activity import * 

if __name__ == "__main__":
	json_data = json.loads(open('../../DATA/feature_extraction/alchemy_generated_input.json').read())

	#preprocess activity
	activity_keys_dict = {}
	for activity in json_data:
		preprocess_activity(activity)
		activity['splitkeys'] = ' '.join(activity['splitkeys'])
		activity_keys_dict[activity['title']] = activity['splitkeys']
	
	#tf_idf_handling
	tf_idf = TfidfVectorizer(sublinear_tf=True, stop_words='english')
	tf_idf.fit_transform(activity_keys_dict.values())

	all_tf_idf=numpy.array([])
	for activity in json_data:
		response = tf_idf.transform([activity['splitkeys']])
		for col in response.nonzero()[1]:
			all_tf_idf = numpy.append(all_tf_idf,response[0, col])

	#find median
	median = numpy.median(all_tf_idf)

	#filter the ones that are below median tf-idf values
	allkeys = tf_idf.get_feature_names()
	for activity in json_data:
		dictionary = {}
		response = tf_idf.transform([activity['splitkeys']])
		for col in response.nonzero()[1]:
			dictionary[str(allkeys[col])]=response[0, col]
		filtered_keys = [key for (key,value) in sorted(dictionary.items(),key=operator.itemgetter(1), reverse=True) if value >= median]
		activity['splitkeys'] = list(set(filtered_keys))

	f = open("test.json", "w+")
	f.write(json.dumps(json_data))
	f.close()

