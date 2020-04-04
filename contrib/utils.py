import random
from django.utils.crypto import get_random_string as base_get_random_string


def generate_random_numbers(length):
    """
    Generates random numbers for a given length.
    :param length: Length of the generated random number.
    :return: Int: Generated random number.
    """
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rand = []
    for i in range(length):
        random.shuffle(nums)
        if i != 0:
            rand.append(nums[8 % i])
        else:
            rand.append(nums[i])
    r = ''.join(str(x) for x in rand)
    return int(r)


def generate_random_strings(length):
    allowed_chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return base_get_random_string(length=length, allowed_chars=allowed_chars)
