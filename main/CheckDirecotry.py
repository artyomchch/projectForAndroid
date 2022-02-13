import os

path = "C:/Users/User/Desktop/Study/Diplom/app"
directory =os.walk(path)
# we shall store all the file names in this list
filelist = []

for root, dirs, files in os.walk(path):
# for file in files:
# append the file name to the list

# filelist.append(os.path.join(root, file))
#   filelist.append(file)
     for d in directory:
         print(d)

# print all the file names
for name in filelist:
    print(name)
