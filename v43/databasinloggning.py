""" 
-- Databas med tabeller som används i detta exepel:
CREATE DATABASE webbserver_demo;
USE webbserver_demo;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    description VARCHAR(100) NOT NULL
);

-- Testanvändare
INSERT INTO users (username, password, description)
VALUES
    ('alice', 'katt123', 'Administratör med ansvar för servern'),
    ('bob',   'hund456', 'Vanlig användare som gillar katter'),
    ('carol', 'fisk789', 'Kurssamordnare, jobbar på distans');
-- I verkligheten skulle man inte lagra lösenord i "klartext" på detta sätt, mer om detta senare i kursen, men vi håller exemplet enkelt.
"""
from flask import Flask, session, redirect, url_for, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'


def get_db():
    """Öppnar en ny anslutning till databasen."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='webbserver_demo'
    )


def query(sql, params=(), fetchone=False):
    """Liten hjälpfunktion: kör en fråga och returnerar rader som dict:ar."""
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)  # <- ger dict:ar istället för tupler
        cur.execute(sql, params)
        if fetchone:
            result = cur.fetchone()
        else:
            result = cur.fetchall()
        conn.commit()   # behövs för INSERT/UPDATE/DELETE
        return result
    finally:
        conn.close()    # viktigt: stäng anslutningen!


@app.route('/')
def index():
    username = session.get('username')

    if username:
        # Hämta färsk info från databasen – inte från sessionen!
        user = query(
            'SELECT id, username, description FROM users WHERE username = %s',
            (username,),
            fetchone=True
        )

        if user is None:
            # Användaren finns inte längre – logga ut
            session.clear()
            return redirect(url_for('index'))

        return f'''
            <h1>Välkommen, {user['username']}!</h1>
            <p>Beskrivning: {user['description']}</p>
            <p>Ditt id i databasen: {user['id']}</p>
            <ul>
                <li><a href="/profile">Min profil</a></li>
                <li><a href="/secret">Hemlig sida (kräver inloggning)</a></li>
                <li><a href="/session-info">Visa sessionens innehåll</a></li>
                <li><a href="/logout">Logga ut</a></li>
            </ul>
        '''
    else:
        return '''
            <h1>Inte inloggad</h1>
            <p>Du måste logga in för att se mer.</p>
            <a href="/login">Logga in</a>
        '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query(
            'SELECT id, username, password FROM users WHERE username = %s',
            (username,),
            fetchone=True
        )

        # Kolla att användaren finns OCH att lösenordet stämmer
        if user and user['password'] == password:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return 'Fel användarnamn eller lösenord. <a href="/login">Försök igen</a>'

    return '''
        <h1>Logga in</h1>
        <form method="post">
            Användarnamn: <input type="text" name="username"><br>
            Lösenord:     <input type="password" name="password"><br>
            <input type="submit" value="Logga in">
        </form>
        <p><i>Testa: alice/katt123, bob/hund456, carol/fisk789</i></p>
    '''


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = query(
        'SELECT id, username, description FROM users WHERE username = %s',
        (session['username'],),
        fetchone=True
    )

    return f'''
        <h1>Profil för {user['username']}</h1>
        <p>Id: {user['id']}</p>
        <p>Beskrivning: {user['description']}</p>
        <p><a href="/">Tillbaka</a></p>
    '''


@app.route('/secret')
def secret():
    if 'username' not in session:
        return redirect(url_for('login'))

    return f'''
        <h1>🔒 Hemlig sida</h1>
        <p>Bara {session['username']} kan se detta.</p>
        <p><a href="/">Tillbaka</a></p>
    '''


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/session-info')
def session_info():
    return f"Session data: {dict(session)}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')