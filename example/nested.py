from typedmarshal import MarshalModel, pretty_print_recursive
from typing import List, Optional


class NestedJson(MarshalModel):
    class Friend:
        name: str = ""
        age: Optional[int] = None
        nicknames: Optional[List[str]] = None

    name: str = ""
    age: int = 0
    friends: List[Friend] = []


nj = NestedJson()
nj.load_json(open('nested.json', 'r'))

print('- nested.json -')
pretty_print_recursive(nj)

