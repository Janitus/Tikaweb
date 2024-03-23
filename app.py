from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_wtf.csrf import CSRFProtect
from extensions import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models.user import User
from models.gameround import GameRound
from models.message import Message # Required by db.createall do not remove!
from play import play_bp
from utils.generator import generate_random_letters
from wordlist_processor import preprocess_wordlist
from sqlalchemy.sql import text
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

print("--------- Launching app ---------")

app = Flask(__name__)

# Generated with LLM
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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
    with db.engine.connect() as connection:

        top_scores_sql = text("""
            SELECT score.id, score.score, "user".username AS user_username, score.game_round_id
            FROM score
            JOIN "user" ON "user".id = score.user_id
            ORDER BY score.score DESC
            LIMIT 10
        """)
        top_scores_result = connection.execute(top_scores_sql).fetchall()
        top_scores = [
            {"id": row[0], "score": row[1], "username": row[2], "game_round_id": row[3]}
            for row in top_scores_result
        ]

        messages_sql = text("""
            SELECT message.content, message.created_at, "user".username AS user_username
            FROM message
            JOIN "user" ON "user".id = message.user_id
            ORDER BY message.created_at DESC
            LIMIT 30
        """)
        messages_result = connection.execute(messages_sql).fetchall()
        messages = [{"content": row[0], "created_at": row[1], "username": row[2]} for row in messages_result]
    

    return render_template('index.html', top_scores=top_scores, messages=messages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        sql = text('INSERT INTO "user" (username, password_hash) VALUES (:username, :password_hash)')

        
        with db.engine.begin() as connection:
            connection.execute(sql, {"username": form.username.data, "password_hash": hashed_password})
        
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        sql = text('SELECT id, username, password_hash FROM "user" WHERE username = :username')

        
        user_dict = None
        with db.engine.connect() as connection:
            result = connection.execute(sql, {"username": form.username.data}).fetchone()
            if result:
                user_dict = {"id": result[0], "username": result[1], "password_hash": result[2]}

        if user_dict and check_password_hash(user_dict['password_hash'], form.password.data):
            user_obj = User(id=user_dict['id'], username=user_dict['username'])
            login_user(user_obj, remember=True)
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, please check your credentials!', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    #sql = text("SELECT * FROM user WHERE id = :user_id")
    sql = text('SELECT "id", "username", "password_hash" FROM "user" WHERE "id" = :user_id')
    result = db.session.execute(sql, {'user_id': user_id}).fetchone()
    if result:
        user = User()
        user.id = result[0]
        user.username = result[1]
        user.password_hash = result[2]
        return user
    return None


@app.route("/play", methods=['GET', 'POST'])
@login_required
def play():
    session['score'] = 0
    session['rerolls'] = 0
    session['words'] = session['words'] = int(os.getenv('GUESSES_PER_GAME', '5'))

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
        sql = text('INSERT INTO "message" ("content", "user_id", "created_at") VALUES (:content, :user_id, :created_at)')
        current_time = datetime.utcnow()
        try:
            with db.engine.begin() as connection:
                connection.execute(sql, {"content": content, "user_id": current_user.get_id(), "created_at": current_time})
            return jsonify({"success": True, "message": "Message posted successfully."})
        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "An error occurred while posting the message."})

    return jsonify({"success": False, "error": "Message content is required."})


@app.route('/game_round/<int:game_round_id>')
def game_round_details(game_round_id):
    game_round = GameRound.query.get_or_404(game_round_id)
    guesses = game_round.guesses
    return render_template('game_round_details.html', game_round=game_round, guesses=guesses)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.config['WORDS_LIST'] = preprocess_wordlist('data/wordlist.txt')
    app.run(debug=True) # We're keeping this for autoupdate when code changes. Kinda like nodemon.
