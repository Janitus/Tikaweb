from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    words = ["apina", "banaani", "cembalo"]
    return render_template("index.html", message="Tervetuloa!", items=words)




if __name__ == "__main__":
    app.run(debug=True) # We're keeping this for autoupdate when code changes. Kinda like nodemon.
