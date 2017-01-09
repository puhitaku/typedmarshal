from typedmarshal import MarshalModel
from typing import List, Dict, Optional, Any, Union


class Trello(MarshalModel):
    class Prefs:
        permissionLevel: str = ""
        voting: str = ""
        comments: str = ""
        invitations: str = ""
        selfJoin: bool = False
        cardCovers: bool = False
        cardAging: str = ""
        calendarFeedEnabled: bool = False
        background: str = ""
        backgroundImage: Optional = None
        backgroundImageScaled: Optional = None
        backgroundTile: bool = False
        backgroundBrightness: str = ""
        backgroundColor: str = ""
        canBePublic: bool = False
        canBeOrg: bool = False
        canBePrivate: bool = False
        canInvite: bool = False

    class Membership:
        id: str = ""
        idMember: str = ""
        memberType: str = ""
        unconfirmed: bool = False
        deactivated: bool = False

    class Label:
        id: str = ""
        idBoard: str = ""
        name: str = ""
        color: str = ""
        uses: int = 0

    class Card:
        class Badge:
            votes: int = 0
            viewingMemberVoted: bool = False
            subscribed: bool = False
            fogbugz: str = ""
            checkItems: int = 0
            checkItemsChecked: int = 0
            comments: int = 0
            attachments: int = 0
            description: bool = False
            due: Optional = None
            dueComplete: bool = False

        id = ""
        checkItemStates: Optional = None
        closed: bool = False
        dateLastActivity: str = ""
        desc: str = ""
        descData: Optional = None
        idBoard: str = ""
        idList: str = ""
        idMembersVoted: List = []
        idShort: int = 0
        idAttachmentCover: Optional = None
        manualCoverAttachment: bool = False
        idLabels: List = []
        name: str = ""
        pos: Union[int, float] = 0
        shortLink: str = ""
        badges: Badge = []
        dueComplete: bool = False
        due: Optional = None
        email: str = ""
        idChecklists: List = []
        idMembers: List = []
        labels: List = []
        shortUrl: str = ""
        subscribed: bool = False
        url: str = ""
        attachments: List = []
        pluginData: List = []

    class Member:
        id: str = ""
        avatarHash: Optional = None
        bio: str = ""
        bioData: Optional[Dict] = None
        confirmed: bool = False
        fullName: str = ""
        idPremOrgsAdmin: List = []
        initials: str = ""
        memberType: str = ""
        products: List[int] = []
        status: str = ""
        url: str = ""
        username: str = ""

    class TList:
        id: str = ""
        name: str = ""
        closed: bool = False
        idBoard: str = ""
        pos: int = 0
        subscribed: bool = False

    class Action:
        class MemberCreator:
            id: str = ""
            avatarHash: Optional = None
            fullName: str = ""
            initials: str = ""
            username: str = ""

        id: str = ""
        idMemberCreator: str = ""
        data: Dict = dict()
        type: str = ""
        date: str = ""
        memberCreator: MemberCreator = MemberCreator()

    id: str = ""
    name: str = ""
    desc: str = ""
    descData: Optional = None
    closed: bool = False
    idOrganization: Optional = None
    invited: bool = False
    pinned: bool = False
    starred: bool = False
    url: str = ""
    prefs: Prefs = None
    invitations: List = []
    memberships: List[Membership] = []
    shortLink: str = ""
    subscribed: bool = False
    labelNames: Dict[str, str] = dict()
    powerUps: List = []
    dateLastActivity: str = ""
    dateLastView: str = ""
    shortUrl: str = ""
    idTags: List = []
    checklists: List = []
    pluginData: List = []
    labels: List[Label] = []
    cards: List[Card] = []
    members: List[Member] = []
    lists: List[TList] = []
    actions: List[Action] = []

trello = Trello()
trello.load_json(open('trello.json'))
print()