import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="1435",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

app = Flask(__name__)

@app.route('/static/css/<path:filepath>')
def serve_css(filepath):
    return app.send_static_file(f'css/{filepath}')


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                return render_template('login.html', error_message='Enter login and password')

            cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if len(records) == 0:
                return render_template('login.html', error_message='User is not found')

            return render_template('account.html', full_name=records[0][1], username=username, password=password)
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html', error_message='')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        try:
            cursor.execute('INSERT INTO users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
        except Exception as e:
            return render_template('registration.html', error_message='Register error: ' + str(e))

    return render_template('registration.html')


if __name__ == '__main__':
    app.run()


