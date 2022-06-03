from ratcliff import ratcliff

def test1():
    assert ratcliff("MATHEMATICS", "MATEMATICA") == 18/21
    assert ratcliff("a", "b") == 0
    assert ratcliff("acommodation", "accommodation") == .96

def testOneSided():
    s1 = "gestalt pattern matching"
    s2 = "gestalt practice"
    assert ratcliff(s1, s2) == 24/40
    assert ratcliff(s2, s1) == 26/40
