import random
import string

def generate_random_letters():
    return random.choices(string.ascii_lowercase, k=10)
