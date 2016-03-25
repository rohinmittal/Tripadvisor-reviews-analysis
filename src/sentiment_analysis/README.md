*****
Data Set:
*****
data_test.json >> test data (10% of reviews) 
data_train.json >> training + validation data (80% as train and 10% as validation) 

JSON format as follows:
[
{"review" : "sentiment"},
{"review" : "sentiment"}
]


*****
Train the model:
*****
>>python train_model.py

This will train the Naive Bayes classifier. Since the training sample will be shuffled every time the model is trained, we are dumping the classifier as "classifier.pickle" to keep track of the most optimized classifier


*****
Test the model:
*****
>>python test_model.py
This will use the classifier.pickle file and test the reviews in data_test.json file.

>>python test_model.py "review"
This fille will take an individual review from command line and display it's sentiment as positive / negative
