### Notes on `fingerprinters` module structure:
1. The `pybel/` sub-module depends on code exposed via the high-level `pybel`
library (a wrapper around openbabel).
2. The `spectrophore` file (and class) leans on `openbabel`, which is the
underlying C++ implementation of the `pybel` interface. Read more about 
`spectrophores` here: 
 *. https://openbabel.org/docs/dev/Fingerprints/spectrophore.html#spectrophores
3. The `pybel/io.py` file is a mixin that will enable various pybel-based
IO operations (like converting input SMiLES str to pybel Molecule object),
it is used via multiple-inheritance, and dependency-injected into the
PybelFingerprinter and SpectrophoreFingerprinter classes.


### Notes on Fingerprints:

1. A Fingerprint is a dense bit-vector, that encodes the presense of patterns
in a given molecule. 
2. Each pattern is typically encoded as 4 or 5 bit vector.
3. Each pattern is logically OR-ed with the Fingerprint vector, to mark the
presence of that particular pattern.
  *. If a pattern is present in a Fingerprint, then ALL 5-bits must be set in
  the Fingerprint vec.
  *. The **converse** is not true: if ALL 5-bits representing a pattern are set
  "ON" in a Fingerprint vec, the pattern is NOT NECCESARILY in the Fingerprint.
  *. The **contrapositive** tells a different story! If ANY of the 5-bits are
  NOT "ON" in the Fingerprint vec, than the pattern is NOT PRESENT in the FP.
  *. Fingerprints are *folded*: cut in half, and logically-OR'ed together, to
  increase information-density and reduce size.
  *. This preserves the given hypothesis above.
  *. It does, however, decrease the chances of finding a 0-bit, thus further
  limiting our ability to use the **contrapositive** to extract information
  about "unimportant patterns", as we cannot, as frequently, find 0-bits that
  indicate a group of patterns are not present.
