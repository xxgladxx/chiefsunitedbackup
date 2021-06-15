from box import Box, BoxList

from .utils import API

API_ENDPOINTS = API('https://api.royaleapi.com')

__all__ = [
    'BaseAttrDict', 'Refreshable', 'PartialTournament',
    'PartialClan', 'PartialPlayer', 'PartialPlayerClan',
    'Member', 'FullPlayer', 'FullClan', 'rlist'
]


class BaseAttrDict:
    """This class is the base class for all models, its a
    wrapper around the `python-box`_ which allows access to data
    via dot notation, in this case, API data will be accessed
    using this class. This class shouldnt normally be used by the
    user since its a base class for the actual models returned from
    the client.

    .. _python-box: https://github.com/cdgriffith/Box

    Example
    -------

    Accessing data via dot notation:

    .. code-block:: python
        sample_data = {
            "stats": {
                "maxTrophies": 5724,
                "favoriteCard": {
                    "name": "P.E.K.K.A"
                        }
                    }
                }

        model = SomeModel(client, sample_data)
        x = sample_data['stats']['maxTrophies']
        # Same as
        x = model['stats']['max_trophies']
        # Same as
        x = model.stats.max_trophies

    This functionality allows this library to present API
    data in a clean dynamic way.

    Attributes
    ----------
    raw_data: dict
        The raw data in the form of a dictionary being used
    cached: bool
        Whether or not the data being used is cached data from
        the cache database.
    last_updated: datetime.datetime
        When the data which is currently being used was last updated.
    response: requests.Response or aiohttp.ClientResponse or None
        Response object containing headers and more information. Returns None if cached
    """
    def __init__(self, client, data, response, cached=False, ts=None):
        self.client = client
        self.response = response
        self.from_data(data, cached, ts, response)

    def from_data(self, data, cached, ts, response):
        self.cached = cached
        self.last_updated = ts
        self.raw_data = data
        self.response = response
        if isinstance(data, list):
            self._boxed_data = BoxList(
                data, camel_killer_box=not self.client.camel_case
            )
        else:
            self._boxed_data = Box(
                data, camel_killer_box=not self.client.camel_case
            )
        return self

    def __getattr__(self, attr):
        try:
            return getattr(self._boxed_data, attr)
        except AttributeError:
            try:
                return super().__getattr__(attr)
            except AttributeError:
                return None

    def __getitem__(self, item):
        try:
            return getattr(self._boxed_data, item)
        except AttributeError:
            raise KeyError('No such key: {}'.format(item))

    def __repr__(self):
        _type = self.__class__.__name__
        return "<{}: {}>".format(_type, self.raw_data)


class Refreshable(BaseAttrDict):
    """Mixin class for re requesting data from
    the api for the specific model.
    """
    def refresh(self):
        """(a)sync refresh the data."""
        if self.client.is_async:
            return self._arefresh()
        data, cached, ts, response = self.client.request(self.url, timeout=None, refresh=True)
        return self.from_data(data, cached, ts, response)

    async def _arefresh(self):
        data, cached, ts, response = await self.client.request(self.url, timeout=None, refresh=True)
        return self.from_data(data, cached, ts, response)

    @property
    def url(self):
        endpoint = self.__class__.__name__.lower()
        return '{}/{}/{}'.format(API_ENDPOINTS.BASE, endpoint, self.tag)


class PartialTournament(BaseAttrDict):
    def get_tournament(self):
        return self.client.get_player(self.tag)


class PartialClan(BaseAttrDict):
    def get_clan(self):
        """(a)sync function to return clan."""
        try:
            return self.client.get_clan(self.clan.tag)
        except AttributeError:
            try:
                return self.client.get_clan(self.tag)
            except AttributeError:
                raise ValueError('This player does not have a clan.')


class PartialPlayer(BaseAttrDict):
    def get_player(self):
        """(a)sync function to return player."""
        return self.client.get_player(self.tag)


class PartialPlayerClan(PartialClan, PartialPlayer):
    """Brief player model,
    does not contain full data, non refreshable.
    """
    pass


class Member(PartialPlayer):
    """A clan member model,
    keeps a reference to the clan object it came from.
    """
    def __init__(self, clan, data, response):
        self.clan = clan
        super().__init__(clan.client, data, response)


class FullPlayer(Refreshable, PartialClan):
    """A clash royale player model."""
    pass


class FullClan(Refreshable):
    """A clash royale clan model, full data + refreshable."""
    def from_data(self, data, cached, ts, response):
        super().from_data(data, cached, ts, response)
        self.members = [Member(self, m, self.response) for m in data.get('members', [])]


class rlist(list, Refreshable):
    def __init__(self, client, data, cached, ts, response):
        self.client = client
        self.from_data(data, cached, ts, response)

    def from_data(self, data, cached, ts, response):
        self.cached = cached
        self.last_updated = ts
        self.response = response
        super().__init__(data)
        return self

    @property
    def url(self):
        return '{}/endpoints'.format(API_ENDPOINTS.BASE)
