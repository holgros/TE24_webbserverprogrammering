"""
CREATE DATABASE webbserver_demo;
USE webbserver_demo;

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    text VARCHAR(255) NOT NULL
);
"""
from flask import Flask, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='webbserver_demo'
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Läs in formulärdata
        name = request.form['name']
        text = request.form['text']

        # Spara i databasen
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO posts (name, text) VALUES (%s, %s)',
            (name, text)
        )
        conn.commit()
        conn.close()

        # Skicka tillbaka användaren till GET-sidan (undvik omsändning)
        return redirect(url_for('index'))

    # GET: hämta alla inlägg och visa formulär + lista
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT name, text FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    conn.close()

    rows = ''.join(
        f'<li><b>{p["name"]}</b>: {p["text"]}</li>' for p in posts
    )

    return f'''
        <h1>Nytt inlägg</h1>
        <form method="post">
            Namn: <input type="text" name="name"><br>
            Text: <input type="text" name="text"><br>
            <input type="submit" value="Spara">
        </form>

        <h2>Inlägg</h2>
        <ul>{rows}</ul>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')