import io
import sys
import json


# Data from the Machine Learning: 
file = raw_input("Directory of the json file to analyze :: ")
f = io.open(file, 'r', encoding='utf8')
data_json = f.read()
data = json.loads(data_json)
f.close()

operator_list = []

for i in data.keys() :
	if (data[i]['Operator'] not in operator_list) :
				operator_list.append(data[i]['Operator'])	


with io.open("operator.txt","w", encoding='utf8') as file2:
	for item in operator_list:
		file2.write('%s\n'% item)
