import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

database = "site.db"

def get_db_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """creating tables."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()


init_db()

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/main')
def home():
    recommended_movies = [
        {"thumbnail": "https://img.youtube.com/vi/YoHD9XEInc0/hqdefault.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"},
        {"thumbnail": "https://img.youtube.com/vi/WIrMeVa0Fzc&t=78s/hqdefaul.jpg"}
    ]
    
    new_movies = []

    hotter_one_movies = []
    return render_template("main.html", recommended_movies=recommended_movies,new_movies=new_movies,hotter_one_movies=hotter_one_movies)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        conn.close()

    return render_template("signUp.html")

@app.route('/signIn', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for())
    return  render_template("signIn.html")

@app.route('/logOut')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' in session:
       return render_template("profile.html") 
    else:
        return redirect(url_for('signUp'))
    return render_template("profile.html")




if __name__ == '__main__':
    app.run(debug=True,port=8000)
