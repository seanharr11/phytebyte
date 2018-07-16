from .binary_classifier_input import (
    NumpyBinaryClassifierInput, BitarrayBinaryClassifierInput)


class BinaryClassifierInputFactory():
    def create(self, encoding: str, positives, negatives, *args, **kwargs):
        if encoding == 'numpy':
            return NumpyBinaryClassifierInput(
                positives=positives,
                negatives=negatives)
        elif encoding == 'bitarray':
            return BitarrayBinaryClassifierInput(
                positives=positives,
                negatives=negatives)
        else:
            raise NotImplementedError(encoding)
