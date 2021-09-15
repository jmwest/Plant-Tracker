import time
import sys
import threading
import queue

def save(message, foo):
    print(message)
    return foo

def exit_f():
    sys.exit()

# Thread1 function
def get_user_input():
    my_bool = True
    while my_bool:
        if input() == 'save':
            print('\nExiting thread.')
            sys.exit()

# Thread 2 function
def multiply():
    pass

# Function to read variables from the save file
def read_save(save_dic):
    try:
        file = open('save.txt', 'r')
    except:
        return False
    save_dic['x'] = file.readline()
    file.close()
    return True

# Function to write variables to the save file
def write_save(save_dic):
    try:
        file = open('save.txt', 'w')
    except:
        return False
    file.write(str(save_dic['x']))
    file.close()
    return True

dic = {}

thread1 = threading.Thread(target=get_user_input)
thread1.daemon = True
thread1.start()

x = 0
if read_save(dic):
    x = int(dic['x'])
else:
    print('File does not exist.\n')
y = 10
while x < y+1:
    print('{:3.0f}'.format((x/y)*100), ' percent complete.\r', end = '', flush=True)
    if not thread1.is_alive():
        dic['x'] = x
        print('\nSaving...\nExit.')
        if not write_save(dic):
            print('Only print when save fails')
        exit_f()
    time.sleep(2)
    x = x + 1

print('\nComplete!')
