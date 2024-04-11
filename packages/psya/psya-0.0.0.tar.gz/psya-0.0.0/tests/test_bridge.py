from psya.mut.bridge import Bridge
from psya.mut.evaluation import Evaluation, pin
from psya.mut.ref import Ref

def test_bridge_pins():
  bridge = Bridge()

  a, b, c, d = map(list, 'abcd')
  ra, rb, rc, rd = map(Ref, (a, b, c, d))

  with Evaluation() as first:    
    pa, pb, pc, pd = map(pin, (ra, rb, rc, rd))
  assert first.pins == set((ra, rb, rc, rd))

  with Evaluation() as second:
    for x in map(Ref, (a, d)): pin(x)
  assert second.pins == set((ra, rd))

  bridge.pin('first', first.pins)
  for x in (pa, pb, pc, pd): assert x in bridge
  
  assert tuple(map(bridge.deref, (pa, pb, pc, pd))) == (ra, rb, rc, rd)
  bridge.pin('second', second.pins)
  assert tuple(map(bridge.deref, (pa, pb, pc, pd))) == (ra, rb, rc, rd)
  bridge.drop('first')

  # at this point, only pins held by the second evaluation should
  # be around
  for x in (pa, pd): assert x in bridge
  for x in (pb, pc): assert x not in bridge

