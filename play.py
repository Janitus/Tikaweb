from flask import Blueprint, request, jsonify, current_app, session
from utils.generator import generate_random_letters
from collections import Counter

play_bp = Blueprint('play_bp', __name__)

@play_bp.route('/reroll', methods=['GET'])
def reroll():
    session['rerolls'] += 1
    session['score'] -= 3 * session['rerolls']

    letters = generate_random_letters()
    session['letters'] = letters
    return jsonify({'letters': letters, 'score': session['score']})

@play_bp.route('/check_word', methods=['POST'])
def check_word():
    data = request.json
    word = data.get('word', '').lower()

    letters_list = session.get('letters', [])
    words_list = current_app.config['WORDS_LIST']

    in_words_list = word in words_list
    can_form = can_form_word(word, letters_list)

    if in_words_list and can_form:
        is_valid = True
        session['score'] = session.get('score', 0) + (len(word) - 2) ** 2
        new_letters = generate_random_letters()
        session['letters'] = new_letters
    else:
        is_valid = False
        new_letters = letters_list

    if not can_form:
        reason = "Can't form word with given letters."
    elif not in_words_list:
        reason = "Word not in list."

    response_data = {
        'isValid': is_valid,
        'score': session.get('score', 0),
        'letters': ' '.join(new_letters)
    }

    if not is_valid:
        response_data['reason'] = reason

    return jsonify(response_data)



def can_form_word(word, letters):
    word_count = Counter(word)
    letters_count = Counter(letters)
    return all(word_count[char] <= letters_count[char] for char in word_count)