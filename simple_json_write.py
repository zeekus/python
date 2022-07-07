# Python program to write JSON to a file

import json

# Data to be written
dictionary ={
	"label" : "blue1",
	"x" : 56,
	"y" : 6,
	"pixel color" : ""
}

# Serializing json
json_object = json.dumps(dictionary, indent = 4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
	outfile.write(json_object)
