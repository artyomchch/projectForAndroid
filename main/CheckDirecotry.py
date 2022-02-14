import os

path = "C:/Users/User/Desktop/Study/Diplom/app/"


def main_ex_app(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            print(d)
            for (root, dirs, file) in os.walk(path + d):
                for f in file:
                    if '.apk' in f:
                        print(f)
