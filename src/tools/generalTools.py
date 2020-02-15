import os


def checkRealPath(path):
    if isinstance(path, str):
        if os.path.isfile(path):
            return True
        else:
            return False
    else:
        return False