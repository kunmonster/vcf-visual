from enum import Enum


class XAxis(Enum):
    """ Enum for XAxis """
    CHR = "CHR"
    MAF = "MAF"
    AF = "AF"
    LEN = "LEN"
    TYPE = "TYPE"
    COUNT = "COUNT"
    DENSITY = "DENSITY"


def validate_x_keys(keys):
    valid_keys = {e.value for e in XAxis}  # 提取所有枚举值
    invalid_keys = [key for key in keys if key not in valid_keys]
    if invalid_keys:
        raise ValueError(f"Invalid keys found: {invalid_keys}. Allowed keys are: {valid_keys}")

