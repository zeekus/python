import os
myfile="target_this_file.py"

print(f'File name: {(os.path.basename(__file__))}')
print(f"We are searching for file with the name '{myfile}'")
print(f' Absolute File name0: {(os.path.abspath(__file__))}') #not not accurate if use os.chdir("..") 
os.chdir("..")
print(f'erronous - Absolute File name1: {(os.path.abspath(__file__))}') #example
os.chdir("..")
print(f'erronous - Absolute File name2: {(os.path.abspath(__file__))}') #not not accurate if use os.chdir("..") before run
print(f"start search path is '{os.getcwd()}'" )

#for root, dirs, files, in os.walk(r'python'):
for root, dirs, files, in os.walk(os.getcwd()):
  #for r in root: 
  #  print(r)
  #for d in dirs:
  #   print(d)
     for name in files:
       if name == myfile:
        print("found: ",end="")
        print(os.path.abspath(os.path.join(root,name)))
