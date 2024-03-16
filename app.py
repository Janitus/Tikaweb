from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return "Registration Page Placeholder"

@app.route('/login')
def login():
    return "Login Page Placeholder"

@app.route('/logout')
def logout():
    return "Logout Page Placeholder"



if __name__ == "__main__":
    app.run(debug=True) # We're keeping this for autoupdate when code changes. Kinda like nodemon.
