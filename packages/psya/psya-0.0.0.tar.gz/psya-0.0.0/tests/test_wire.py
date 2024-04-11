from psya.wire import Json

def reflect(*args, **kwargs): return args, kwargs

def test_wire_static():
  wire = Json()
  encoded_fn = wire.encode(test_wire_static)
  assert encoded_fn == """
    {"__class__":"builtins:function","$static":"tests.test_wire:test_wire_static"}
  """.strip()
  assert wire.decode(encoded_fn) is test_wire_static

  assert wire.decode("""
    {"$static": "tests.test_wire:reflect",
     "0": "pos arg 1",
     "1": "pos arg 2",
     "some_kw": "a value",
     "other_kw": 42}
  """)() == (("pos arg 1", "pos arg 2"), {"some_kw": "a value", "other_kw": 42})