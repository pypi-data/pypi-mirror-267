class RichSplitError(Exception):
    pass


class CutError(RichSplitError):
    pass


class JoinError(RichSplitError):
    pass
