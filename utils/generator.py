import random
import string

def generate_random_letters():
    best = ['a','e','i']
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [letter for letter in string.ascii_lowercase if letter not in vowels]

    bests = random.choices(best, k=1)
    vowels = random.choices(vowels, k=1)
    third = random.choices(consonants, k=1)
    remaining_letters = random.choices(string.ascii_lowercase, k=8)
    letters = bests + vowels + third + remaining_letters
    random.shuffle(letters)
    return letters
