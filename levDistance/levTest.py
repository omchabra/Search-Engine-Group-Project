from levDist import levDist

def testMain():

    assert levDist("sitting", "kitten") == 3
    assert levDist("junk", "clunky") == 3
    assert levDist("random123", "rbnqor321") == 5
    
    
    assert levDist("hi", "HI") == 0
    assert levDist("hi", "hil") == 1
    assert levDist("hi", "HIL") == 1
