import random

def random_capitalize(s: str, probability: float=0.5):
    return ''.join([c.upper() if random.random() < probability else c for c in s])

