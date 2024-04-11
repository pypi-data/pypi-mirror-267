from psya.the import the

def test_the():
  with the(str, "hello there"):
    with the(int, 42):
      assert the[str] == "hello there"
      assert the[int] == 42
    assert the[str] == "hello there"
    assert the.get(int, None) is None
  