from typing import List
from typedmarshal import MarshalModel


class SampleModel(MarshalModel):
    name: str = None
    age: int = None
    hobbies: List[str] = []

js_str = '''
{
    "name": "Hatsune Miku",
    "age": 16,
    "hobbies": ["Sing a song", "Dance to music", "Eat negi"]
}
'''

js_obj = SampleModel()
js_obj.load_json(js_str)
print(js_obj.name)
print(js_obj.hobbies)