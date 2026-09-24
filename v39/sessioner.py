
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Används för sessionshantering

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session[request.form['name']] = request.form['text'] # Så här sätter man värde på en sessionsvariabel.
        return redirect(url_for('index'))
    
    # Det här returneras om GET-anrop görs
    return f'''
        <form method="post">
            Enter text: <input type="text" name="name" value=""><br>
            Enter text: <input type="text" name="text" value="">
            <input type="submit" value="Set">
        </form>
        <p>Session value:</p>
        <a href="/clear">Clear session value</a>
        <br><a href="/session-info">Show session info</a>
    '''

@app.route('/clear')
def clear():
    # Man behöver inte ange köra både .pop() och .clear() för att ta bort sessionsvariabler. Detta är bara för att visa alternativen.
    session.pop('text', None)  # Så här tar man bort EN sessionsvariabel.
    session.clear()  # Så här tar man bort ALLA sessionsvariabler.
    return redirect(url_for('index'))

@app.route('/session-info')
def session_info():
    # Skickar tillbaka all session data som respons.
    return f"Session data: {dict(session)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
