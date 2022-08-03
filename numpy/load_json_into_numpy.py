import json

def  load_data_from_json(path,json_file):
  f=open(json_file)        #open file
  data = json.load(f)      #load json data into mem
  f.close                  #close file

  main_array=[]
  extra_array=[]
  #loop through the json data assign fields to variables
  for i in data:
    main=i['main']
    extra=i['extra']
    mydate=i['drawing_date']
    main_array.append(main)
    extra_array.append(extra)

  return main_array,extra_array

path=""
json_file="mnumbers.json"
r1,r2=load_data_from_json(path,json_file)
print(str(r1))
print(str(r2))