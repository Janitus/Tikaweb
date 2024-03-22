from flask import Blueprint, request, jsonify, current_app, session
from utils.generator import generate_random_letters
from collections import Counter

play_bp = Blueprint('play_bp', __name__)

@play_bp.route('/reroll', methods=['GET'])
def reroll():
    print("Reroll penalty!")
    session['rerolls'] += 1
    session['score'] -= 3 * session['rerolls']

    letters = generate_random_letters()
    session['letters'] = letters
    return jsonify({'letters': letters, 'score': session['score']})

@play_bp.route('/check_word', methods=['POST'])
def check_word():
    if session.get('words', 0) <= 0:
        return jsonify({'gameOver': True, 'message': 'Game over, no more attempts left.'}), 200

    data = request.json
    word = data.get('word', '').lower()

    letters_list = session.get('letters', [])
    words_list = current_app.config['WORDS_LIST']

    in_words_list = word in words_list
    can_form = can_form_word(word, letters_list)

    is_valid = update_game_state(word, in_words_list, can_form)

    response_data = generate_response_data(is_valid, word, in_words_list, can_form)

    return jsonify(response_data)

def update_game_state(word, in_words_list, can_form):
    if in_words_list and can_form:
        session['score'] += (len(word) - 2) ** 2
        is_valid = True
    else:
        is_valid = False

    session['words'] -= 1
    session['letters'] = generate_random_letters()

    return is_valid

def generate_response_data(is_valid, word, in_words_list, can_form):
    if not can_form:
        reason = "Can't form word with given letters."
    elif not in_words_list:
        reason = "Word not in list."

    response_data = {
        'isValid': is_valid,
        'score': session.get('score', 0),
        'letters': ' '.join(session['letters']),
        'attemptsLeft': session.get('words', 0)
    }

    if not is_valid:
        response_data['reason'] = reason

    if session['words'] <= 0:
        response_data['gameOver'] = True

    return response_data

def can_form_word(word, letters):
    word_count = Counter(word)
    letters_count = Counter(letters)
    return all(word_count[char] <= letters_count[char] for char in word_count)