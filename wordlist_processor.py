import re

def preprocess_wordlist(file_path):
    print("Checking if the word file needs cleaning.")
    discarded_count = 0
    valid_words = []

    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip().lower()
            if len(word) > 2 and re.match('^[a-z]+$', word):
                valid_words.append(word)
            else:
                discarded_count += 1

    with open(file_path, 'w') as file:
        for word in valid_words:
            file.write(word + '\n')

    if discarded_count > 0:
        print(f"Discarded {discarded_count} words from the file.")
    else:
        print("No words discarded from the text file.")

    print(f"Amount of valid words {len(valid_words)} in the game.")
    return valid_words
