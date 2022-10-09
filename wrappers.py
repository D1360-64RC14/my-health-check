from datetime import datetime
from sys import stderr

def print_exception(err: Exception):
    print(err, file=stderr)

def time_now():
    return datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
