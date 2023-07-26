#!/usr/bin/env python

import logging
import os

from flask import Flask, request, session, redirect, url_for, make_response

logging.basicConfig()

os.environ['FLASK_DEBUG'] = 'true'

app = Flask(__name__)

# IF THIS IS A SECRET IT SHOULD BE HASHED AND STORED SAFELY NOT HARDCODED
# FILE_SECRET = 'h20tavyWvchAlZko21t0X0lH93VJCQBn'
app.secret_key = 'h20tavyWvchAlZko21t0X0lH93VJCQBn'

# ---------------------- MISSING HOME PAGE ----------------------------
# @app.route('/')
# def home():
    # return 'Welcome to the HomePage!'
# 
# @app.route('/about')
# def about():
    # return 'This is the About page.'
# 
# @app.route('/contact')
# def contact():
    # return 'Contact us at contact@example.com.'

# ---------------------- MISSING HOME PAGE ----------------------------

# @app.route('/image/<file_name>', methods=['GET'])
# def get_image(file_name):
    # secret = request.args['X-Image-Secret']
    # print(secret)
# 
    # with open(f'images/{file_name}.png', 'rb') as f:
        # if secret != FILE_SECRET:
            # logging.info(f'bad file secret! {secret}')
            # return '', 403
# 
        # return f.read()
# 
# 
# @app.route('/image/<file_name>', methods=['POST'])
# def save_image(file_name):
    # secret = request.headers['X-Image-Secret']
    # print(secret)
    # with open(f'images/{file_name}.png', 'wb') as f:
        # if secret != FILE_SECRET:
            # logging.info(f'bad file secret! {secret}')
            # return '', 403
# 
        # f.write(request.data)
# 
        # return ''

# ------------------------- HELPFUL LINKS------------------------------
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

# https://blog.logrocket.com/build-deploy-flask-app-using-docker/

# https://stackoverflow.com/questions/11017466 flask-to-return-image-stored-in-database

# ----------------------------------- START OF CODE -----------------------------
# Simulated user data -> probably could come from a DB. 
USERS = {
    'user1': {'password': 'password123', 
              'name': 'Kevin', 
              'secret_key': 'h20tavyWvchAlZko21t0X0lH93VJCQBn'
              }
}

# Login Page to get user/password and get secret key for session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].casefold()
        password = request.form['password']
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))

    return '''
        <form method="post">
            <p><input type="text" name="username" placeholder="Username"></p>
            <p><input type="password" name="password" placeholder="Password"></p>
            <p><input type="submit" value="Log In"></p>
        </form>
    '''

# Logout button to clear session and redirect to login screen.
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Default Welcome Page for Auth Users. Also has basic guidance on other capabilities the app has
@app.route('/')
def home():
    if 'username' in session:
        return f'''
            Welcome, {USERS[session["username"]]["name"]}! 
            <a href="/logout">Log out</a><br>
            <h3>For More Info Visit</h3>
            <h4>URL: /images/image100-199</h4>
            '''
    else:
        return redirect(url_for('login'))

# This will provided the image that the user chooses, will redirect if username no longer in session to login screen.
@app.route('/images/<file_name>', methods=['GET'])
def get_image(file_name):
    if 'username' in session:
        secret_key = USERS[session['username']]['secret_key']
        # if 'X-Image-Secret' in request.headers and request.headers['X-Image-Secret'] == secret_key:  <--- Do not know how to fix this...
        
        # checking the secret key vs secret_key for user for access.
        if app.secret_key == secret_key:
            # open the image in binary
            with open(f'images/{file_name}.png', 'rb') as f:  # <-- Add '.png' extension
                response = make_response(f.read())
                response.headers['Content-Type'] = 'image/png' # <--- Display png correctly to user
                return response
            
        else:
            return '', 403  # Forbidden, invalid secret key or missing header
    else:
        return redirect(url_for('login'))

# app.run('localhost', port=3000)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run('0.0.0.0', port=port)
# 