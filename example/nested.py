from typedmarshal import MarshalModel, pretty_print_recursive
from typing import List, Optional


class Friend:
    name: str = None
    age: int = None
    nicknames: Optional[List[str]] = None


class NestedJson(MarshalModel):
    name: str = None
    age: int = None
    friends: List[Friend] = []


nj = NestedJson()
nj.load_json(open('nested.json', 'r'))

print('- nested.json -')
pretty_print_recursive(nj)

