from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_wtf.csrf import CSRFProtect
from extensions import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models.user import User
from models.score import Score
from models.message import Message
from models.gameround import GameRound
from play import play_bp
from utils.generator import generate_random_letters
import re


print("--------- Launching app ---------")

app = Flask(__name__)

# Generated with LLM
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# End Gen

csrf = CSRFProtect(app)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(play_bp)



# Routes

@app.route("/")
def index():
    top_scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    messages = Message.query.order_by(Message.created_at.desc()).limit(30).all()
    return render_template('index.html', top_scores=top_scores, messages=messages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, please check your credentials!', 'danger')
            return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/play", methods=['GET', 'POST'])
@login_required
def play():
    session['score'] = 0
    session['rerolls'] = 0
    session['words'] = 15

    new_round = GameRound(player_id=current_user.id)
    db.session.add(new_round)
    db.session.commit()

    session['game_round_id'] = new_round.id

    letters = generate_random_letters()
    session['letters'] = letters
    
    return render_template('play.html', letters=letters)


@app.route("/post_message", methods=['POST'])
@login_required
def post_message():
    data = request.get_json()
    content = data.get('content')

    if len(content) > 100:
        return jsonify({"success": False, "error": "Message content exceeds the maximum allowed length."})

    if content:
        message = Message(content=content, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        return jsonify({"success": True, "message": "Message posted successfully."})
    return jsonify({"success": False, "error": "Message content is required."})


@app.route('/game_round/<int:game_round_id>')
def game_round_details(game_round_id):
    game_round = GameRound.query.get_or_404(game_round_id)
    guesses = game_round.guesses
    return render_template('game_round_details.html', game_round=game_round, guesses=guesses)



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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.config['WORDS_LIST'] = preprocess_wordlist('data/wordlist.txt')
    app.run(debug=True) # We're keeping this for autoupdate when code changes. Kinda like nodemon.
