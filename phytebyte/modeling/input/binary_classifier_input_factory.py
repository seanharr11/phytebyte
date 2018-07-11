from .binary_classifier_input import NumpyBinaryClassifierInput


class BinaryClassifierInputFactory():
    def create(self, encoding: str, positives, negatives, *args, **kwargs):
        if encoding == 'numpy':
            return NumpyBinaryClassifierInput(
                positives=positives,
                negatives=negatives)
        else:
            raise NotImplementedError(encoding)
