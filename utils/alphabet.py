import random

alphabet = "BCDFGHJKLMNOPQRSTVWXYZ"
vowels = "AEIOU"


def random_letter():
    return random.choice(alphabet + vowels * 3).upper()
