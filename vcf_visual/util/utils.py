

from numbers import Number


def get_unit(num:Number)->str:
    """
    Get the unit of a number
    """
    if num < 1e3:
        return "bp"
    elif num < 1e6:
        return "Kb"
    elif num < 1e9:
        return "Mb"
    else:
        return "b"
    
