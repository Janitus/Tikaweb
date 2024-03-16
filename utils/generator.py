import random
import string

def generate_random_letters():
    # The algorithm is fairly simple and adjustable
    # The best is entirely subjective, but I've chosen some decent letters that will help the player make words with
    # You can also adjust the amount of letters offered by each of them by setting the k=amount

    best = ['a','e','i']
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [letter for letter in string.ascii_lowercase if letter not in vowels]

    bests = random.choices(best, k=2)
    vowels = random.choices(vowels, k=1)
    third = random.choices(consonants, k=1)
    remaining_letters = random.choices(string.ascii_lowercase, k=7)
    letters = bests + vowels + third + remaining_letters
    random.shuffle(letters)
    return letters
