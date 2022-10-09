import time
import schedule
from domain import Domain
from health_check import HealthCheck
import actions

DOMAINS_TO_CHECK: list[Domain] = [
    Domain('http://snapdrop.raspi'),
    Domain('http://ipfs.raspi')
]

hc = HealthCheck()

hc.on('host_down', actions.send_notify)
hc.on('error', actions.error)

schedule.every().hour.at(':00').do(hc.run_checks, DOMAINS_TO_CHECK)

schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)