from httpx import Headers

class Domain:
    _url: str
    header: Headers | None

    def __init__(self, url: str, header: Headers | None = None):
        self._url = url
        self.header = header

    @property
    def url(self):
        return self._url

    def __dict__(self):
        return {
            'url': self._url,
            'header': self.header
        }

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"'Domain <{self.__str__()}>'"