from datetime import datetime
from pyee import EventEmitter
from httpx import Client, Request, Timeout
from domain import Domain

def time_now():
    return datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

class HealthCheck(EventEmitter):
    _client: Client
    _down_domains: dict[Domain, bool]
    _flood: bool

    def __init__(
        self, *,
        client: Client | None = None,
        flood: bool = False
    ):
        # https://pyee.readthedocs.io/en/latest/
        super().__init__()
        self._down_domains = dict()
        self._flood = flood

        if client is None:
            self._client = Client(
                http2=True,
                follow_redirects=True
            )
        else:
            self._client = client

    def _run_check_single(self, domain: Domain):
        req = Request('HEAD', domain.url, headers=domain.header)

        try:
            res = self._client.send(req)
        except Exception as err:
            self.emit('error', err)
            return

        self.emit(str(res.status_code), res)

        is_domain_down = self._down_domains.get(domain)

        if is_domain_down is None:
            self._down_domains.update({
                domain: not res.is_success
            })
            # It invert the status to emit the events on first time
            is_domain_down = not (not res.is_success)

        # Stay the same status
        # If it's down and didn't got success, it is the same status
        if (is_domain_down is (not res.is_success)) and (not self._flood):
            return

        self._down_domains.update({
            domain: not res.is_success
        })

        if res.is_success:
            self.emit('host_up', res)
        else:
            self.emit('host_down', res)

    def run_checks(self, domains: list[Domain] | Domain):
        """
        Checks if listed domains are up. If not, 
        """

        print(f'Running check at {time_now()}...', end=' ')

        if type(domains) is Domain:
            self._run_check_single(domains)

        elif type(domains) is list:
            for domain in domains:
                self._run_check_single(domain)

        print(f'Finished at {time_now()}.')