from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

USERS_FILE = 'Sprint-project-main/data/users.json'

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('profile_create_will'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        if any(user['username'] == username for user in users):
            return render_template('registration.html', error='User with this username already exists.')

        if password != confirm_password:
            return render_template('registration.html', error='Passwords do not match.')

        hashed_password = hash_password(password)

        new_user = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': hashed_password,
            'wills': []
        }

        users.append(new_user)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)

        session['user'] = new_user
        return redirect(url_for('profile_create_will'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('profile_create_will'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hash_password(password)

        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        user = next((user for user in users if user['username'] == username and user['password'] == hashed_password), None)

        if user is not None:
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)

            user = next((u for u in users if u['username'] == username), None)
            
            session['user'] = user
            return redirect(url_for('profile_create_will'))
        else:
            error = 'Incorrect username or password.'

    return render_template('login.html', error=error)


@app.route('/profile_create_will', methods=['GET', 'POST'])
def profile_create_will():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    if request.method == 'POST':
        will_text = request.json.get('will-text')

        if 'wills' not in user or not isinstance(user['wills'], list):
            user['wills'] = []

        if will_text.strip():
            user['wills'].append(will_text)

            with open(USERS_FILE, 'r') as f:
                users = json.load(f)

            found_user = next((u for u in users if u['username'] == user['username']), None)

            if found_user:
                found_user['wills'].append(will_text)

                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f, indent=2)

                session['user']['wills'] = found_user['wills']

                return jsonify({'will': will_text})

    return render_template('profile_create_will.html', user=user)




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
