from httpx import Response
from subprocess import Popen

def send_notify(res: Response):
    Popen([
        'notify-send',
        '--app-name=DHealthCheck',
        'Health Check',
        'Domain {} is Down! Status code {}'.format(res.url, res.status_code)
    ])