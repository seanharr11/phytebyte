1. Separate tests out b/t base.py and tanimoto_thresh.py
2. Determine how to mock out:
```
class TanimotoThreshNegiatveSampler():
    _input_fingerprinter = Fingerprinter.create("daylight")
```
...so that "Fingerprinter.create()" returns a mock_input_fingerprinter. Right
now we set this value in __init__ so that we can set it. Globals are bad!
