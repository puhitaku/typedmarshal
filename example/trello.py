from typedmarshal import MarshalModel
from typing import List, Dict, Optional


class Trello(MarshalModel):
    id: str = None
    name: str = None
    desc: str = None
    descData = None
    closed: bool = None
    idOrganization = None
    invited: bool = None
    pinned: bool = None
    starred: bool = None
    url: str = None
    prefs: Dict = None
    invitations: List = None
    memberships: List[Dict] = None
    shortLink: str = None
    subscribed: bool = None
    labelNames: Dict = None
    powerUps: List = None
    dateLastActivity: str = None
    dateLastView: str = None
    shortUrl: str = None
    idTags: List = None
    checklists: List = None
    pluginData: List = None
    labels: List[Dict] = None
    cards: List[Dict] = None
    members: List[Dict] = None
    lists: List[Dict] = None
    actions: List[Dict] = None
