import datetime
from pynput import keyboard 


def get_now():
    return datetime.datetime.now()

def flush_input():
    import sys, termios
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def file_append(file_path, target_string):
    f = open(file_path, 'a')
    f.write(target_string)
    f.close()


current_pressed = set()
file_path = './key.log'

def on_press(key): 
    current_pressed.add(key)

    str = '%s pressed\n' % current_pressed
    file_append(file_path, str)
    
def on_release(key): 
    str = '%s released\n' %key
    file_append(file_path, str)
    
    if key == keyboard.Key.esc:
        flush_input()
        return False 
    if key in current_pressed: 
        current_pressed.remove(key) 
        
with keyboard.Listener( 
    on_press=on_press, 
    on_release=on_release) as listener: 
    listener.join()
