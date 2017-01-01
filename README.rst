TypedMarshal
============

Strongly typed (un)marshaller between Python object and JSON inspired by Golang's "encode/json" library.


Short example
-------------

Here is a pitch for TypedMarshal.

Let there be a JSON model definition: ::

    from typedmarshal import MarshalModel

    class SampleModel(MarshalModel):
        name: str = None
        age: int = None
        hobbies: List[str] = []

Then unmarshal JSON: ::

    js_str = '''
    {
        "name": "Hatsune Miku",
        "age": 16,
        "hobbies": ["Sing a song", "Dance to music", "Eat negi"]
    }
    '''

    js_obj = SampleModel()
    js_obj.load_json(js_str)

Now defined attributes are available to use: ::

    >>> js_obj.name
    'Hatsune Miku'

    >>> js_obj.hobbies
    ['Sing a song', 'Dance to music', 'Eat negi']

Voila!


Development progress
--------------------

It's still in alpha and unstable. Everything may change in future.


Contributing
------------

TBD


License
-------

This library is released under BSD License.
