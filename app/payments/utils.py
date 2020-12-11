import hashlib
import hmac
import sys


def verify_signature(body, signature, key):
    if sys.version_info[0] == 3:  # pragma: no cover
        key = bytes(key, 'utf-8')
        body = bytes(body, 'utf-8')

    dig = hmac.new(key=key,
                   msg=body,
                   digestmod=hashlib.sha256)

    generated_signature = dig.hexdigest()

    if sys.version_info[0:3] < (2, 7, 7):
        result = compare_string(generated_signature, signature)
    else:
        result = hmac.compare_digest(generated_signature, signature)

    return result


# Taken from Django Source Code
# Used in python version < 2.7.7
# As hmac.compare_digest is not present in prev versions
def compare_string(expected_str, actual_str):
    """
    Returns True if the two strings are equal, False otherwise
    The time taken is independent of the number of characters that match
    For the sake of simplicity, this function executes in constant time only
    when the two strings have the same length. It short-circuits when they
    have different lengths
    """
    if len(expected_str) != len(actual_str):
        return False
    result = 0
    for x, y in zip(expected_str, actual_str):
        result |= ord(x) ^ ord(y)
    return result == 0
