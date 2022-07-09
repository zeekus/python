import json,os

def  determine_message(file):
  f=open(file)        #open file
  data = json.load(f) #load json data into mem
  f.close             #close file

  #loop thorough the data
  for i in data:
    message=i['message']
    filename=i['filename']
    #print(i['message'] + "," + i['filename'])
    print(filename + ":" + message)



path=os.getcwd()
myfile=(path + "/messages/messages.json")
determine_message(myfile)


