
########################### get current time ###########################

def get_now():
    import datetime
    
    return datetime.datetime.now()



############################### file io ################################

def flush_input():
    import sys, termios
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def file_append(file_path, target_string):
    f = open(file_path, 'a')
    f.write(target_string)
    f.close()



################### periodic function call decorator ###################
'''
Original code can be found at:
    https://gist.github.com/Depado/7925679
'''


# Function wrapper 
def periodic_task(interval, times = -1):
    import threading
    
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

