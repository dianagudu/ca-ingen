def ispositivefloat(x):
    try:
        return float(x) >= 0
    except ValueError:
        return False


def ispositiveint(x):
    try:
        return int(x) >= 0
    except ValueError:
        return False