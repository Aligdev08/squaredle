import random

BAG = (
    "E" * 12 + "AI" * 9 + "SO" * 8 + "TRNG" * 6 + "LUD" * 4 + "BCMPFHVWY" * 2 + "KJXQZ"
)


def random_letter(bag=BAG):
    return random.choice(bag)
