#filename: find_newest_game_log_file.py
#description: from an abstract search generate a list of all the text files and return the newest file.

class Findgamelog:
   def get_newest_game_file(self,gamelog):
     import subprocess
     import time
     import os
     import glob
     #proc=subprocess.run(['find','/home','-iname','GameLogs'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
     proc=subprocess.run(['find','/home','-iname',gamelog], check=True, stdout=subprocess.PIPE, universal_newlines=True)
     directories=[] #may have more than onesearchedfile
     directories=proc.stdout.rstrip().split("\n")  #generates list - remove white space at end of line and split by whitespace if more than one line
     list_of_files=[]
     print(f"my dirs: '{directories}'")
     for directory in directories:
       print(f"Exending list with '{directory}/*.txt' ")
       list_of_files.extend(glob.glob(directory + "/*.txt")) #append list
       file_count=0
       sorted_list=sorted( list_of_files, key = lambda file: os.path.getmtime(file)) #sort list of files by mtime to get newest
       for file in sorted_list: 
        file_count=file_count+1
        #print(f"\nLast File from list of {file_count} files: {file}")
        #print("{} - {}".format(file, time.ctime(os.path.getctime(file))) )
        return file #return last file


game=Findgamelog()
myfile=game.get_newest_game_file("GameLogs")
print(f"last file is {myfile}")













