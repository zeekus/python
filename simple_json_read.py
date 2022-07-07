# Python program to read
# json file


import json

# Opening JSON file
f = open('screendata.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['screen_points']:
	#remove the unicode from the variables I want.
	print(i['label']) 
	label=json.dumps(i['label'],encoding="ascii")
	RGBPixelColor=json.dumps(i['RGBPixelColor'],encoding='ascii')
	x=json.dumps(i['x'],encoding='ascii')
	y=json.dumps(i['y'],encoding='ascii')
	print(i)
	print(label,x,y,RGBPixelColor)

# Closing file
f.close()
