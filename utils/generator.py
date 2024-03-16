import random
import string

def generate_random_letters():
    # The algorithm is fairly simple and adjustable
    # The best is entirely subjective, but I've chosen some decent letters that will help the player make words with
    # You can also adjust the amount of letters offered by each of them by setting the k=amount

    best_vowels = ['a','e','o'] # top 3 vowels english
    all_vowels = ['a', 'e', 'i', 'o', 'u']
    best_consonants = ['t','n','s','r','h'] # top 5 consonants english

    bests = random.choices(best_vowels, k=2)
    all_vowels = random.choices(all_vowels, k=1)
    third = random.choices(best_consonants, k=3)
    remaining_letters = random.choices(string.ascii_lowercase, k=5)
    letters = bests + all_vowels + third + remaining_letters
    random.shuffle(letters)
    return letters
