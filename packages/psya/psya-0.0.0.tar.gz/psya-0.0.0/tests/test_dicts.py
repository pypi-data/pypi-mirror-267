from psya.dicts import BiDictionary

def test_bidict():
  d = BiDictionary()
  d['first'] = set('abcd')  
  d['second'] = set('bc')
  assert d['first'] == set('abcd')
  d.unlink('first', 'd')
  assert d['first'] == set('abc')
  assert set(d.reverse.keys()) == set('abc')
  del d['first']
  assert set(d.reverse.keys()) == set('bc')