import json
from preprocess_activity import *

if __name__ == "__main__":
	json_data = json.loads(open("../../DATA/feature_extraction/input_golden.json").read())

	for activity in json_data:
		split_keys = split_phrases(activity['ta_phrases'])
		activity['splitkeys'] = list(set(split_keys))

	f = open("golden.json", "w+")
	f.write(json.dumps(json_data))
	f.close()
