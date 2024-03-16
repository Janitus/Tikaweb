from flask import Blueprint, request, jsonify, current_app, session
from utils.generator import generate_random_letters

play_bp = Blueprint('play_bp', __name__)

@play_bp.route('/reroll', methods=['GET'])
def reroll():
    session['rerolls'] += 1
    session['score'] -= 3 * session['rerolls']

    letters = generate_random_letters()
    return jsonify({'letters': letters, 'score': session['score']})

@play_bp.route('/check_word', methods=['POST'])
def check_word():
    data = request.json
    word = data.get('word', '').lower()
    words_list = current_app.config['WORDS_LIST']
    is_valid = word in words_list
    return jsonify({'isValid': is_valid})
