
class TravelState:
    '''This is class defining the travel state'''
    def __init__(self, message):
        self.message = message
    
    def action(self):
        if self.message =='jumping':
            print('stop & wait')
        elif self.message =='warping':
            print('warping/traveling')
        elif self.message =='aligning':
            print('aligning - ready to cloak,jump')
        elif self.message =='approaching':
            print('coming out of warp/approaching')
        elif self.message =='docking':
            print('docking in station')
        elif self.message=='establishing warp vector':
            print('waiting for warp. warping without align')
        else:
            print('unknown message')


class Buttons(object):
    def __init__(self, filename, trigger, description, location=None):
        self.filename   = filename
        self.trigger    = trigger #message
        self.descripton = description
        self.location   = location

class Messages(object):
    def __init__(self, filename, trigger, description, location=None):
        self.filename   = filename
        self.trigger    = trigger #message
        self.descripton = description
        self.location   = location

def  load_target_data_from_json(path,json_file,target_message):
  f=open(json_file)        #open file
  data = json.load(f)      #load json data into mem
  f.close                  #close file

  file_array=[]
  #loop through the json data
  for i in data:
    message=i['message']
    filename=i['filename']
    if i['message'] == target_message:
      #print("appending " + path + "/" + filename )
      file_array.append(path + filename)

  return file_array

message = TravelState('warping')
message.action()

# Creating class objects
for c in ['aligning', 'warping', 'approaching', 'stopped']:
    c = TravelState(c)
    c.action()
    print('\n')