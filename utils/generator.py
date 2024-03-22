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
    all_vowels_choice = random.choices(all_vowels, k=1)
    third = random.choices(best_consonants, k=3)

    chosen_letters = set(bests + all_vowels_choice + third)
    
    remaining_letters = []
    while len(remaining_letters) < 5:
        remaining_letters_pool = [letter for letter in string.ascii_lowercase if letter not in chosen_letters]
        new_letter = random.choice(remaining_letters_pool)
        remaining_letters.append(new_letter)
        chosen_letters.add(new_letter)

    letters = bests + all_vowels_choice + third + remaining_letters
    random.shuffle(letters)
    return letters