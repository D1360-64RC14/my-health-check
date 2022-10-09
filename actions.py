from sys import stderr
from httpx import Response
from subprocess import Popen

def error(err: Exception):
    print(err, file=stderr)

def send_notify(res: Response):
    Popen([
        'notify-send',
        '--app-name=DHealthCheck',
        'Health Check',
        'Domain {} is Down! Status code {}'.format(res.url, res.status_code)
    ])