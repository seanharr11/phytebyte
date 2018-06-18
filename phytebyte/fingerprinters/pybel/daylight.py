from .pybel import PybelFingerprinter


class DaylightFingerprinter(PybelFingerprinter):
    @property
    def _pybel_fp_name(self) -> str:
        return "FP2"
