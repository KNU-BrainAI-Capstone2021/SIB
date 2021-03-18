'''
original code can be found at:
    https://gozz123.tistory.com/31
'''

from pynput import keyboard 

current_pressed = set() 

def on_press(key): 
    current_pressed.add(key) 
    print('Key %s pressed' % current_pressed) 
    
def on_release(key): 
    print('Key %s released' %key) 
    
    if key == keyboard.Key.esc: 
        return False 
    if key in current_pressed: 
        current_pressed.remove(key) 
        
with keyboard.Listener( 
    on_press=on_press, 
    on_release=on_release) as listener: 
    listener.join()
