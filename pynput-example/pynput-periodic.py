'''
original code can be found at:
    https://pynput.readthedocs.io/en/latest/keyboard.html

WARNING - this code does NOT actually scan keyboard input PERIODICALLY
'''

from pynput import keyboard

# The event listener will be running in this block
with keyboard.Events() as events:
    while True:
        # Block at most one second
        event = events.get(1.0)
        
        if event is None:
            print('You did not press a key within one second')
        elif event.key == keyboard.Key.esc:
            break
        else:
            print('Received event {}'.format(event))