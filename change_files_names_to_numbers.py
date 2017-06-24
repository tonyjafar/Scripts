import os
import sys

if len(sys.argv) < 2:
    sys.exit(2)

dir_name = sys.argv[1]
x = 1
for file in os.listdir(dir_name):
    file = os.path.join(dir_name, file)
    if os.path.isfile(file):
        filename, file_extension = os.path.splitext(file)
        os.chdir(dir_name)
        if x <= 9:
            new_name = '00' + str(x) + file_extension
            os.rename(file, new_name)
        elif 9 < x <= 99:
            new_name = '0' + str(x) + file_extension
            os.rename(file, new_name)
        else:
            new_name = str(x) + file_extension
            os.rename(file, new_name)
    x += 1
