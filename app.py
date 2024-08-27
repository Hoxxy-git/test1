from flask import Flask, request, redirect, url_for, render_template_string, escape
import sqlite3
import os

app = Flask(__name__)

# SQLite 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
        <h1>Welcome to the Home Page!</h1>
        <p>Select a page to navigate:</p>
        <button onclick="window.location.href='/login'">Login Page</button><br><br>
        <button onclick="window.location.href='/upload'">Upload Page</button><br><br>
        <button onclick="window.location.href='/greet'">Greet Page</button>
    '''

# SQL Injection 방지된 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        c.execute(query, (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return f'Welcome, {escape(username)}!'
        else:
            return 'Invalid credentials!'

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# 파일 업로드 페이지
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # 사용자 파일 이름에서 경로 관련 요소 제거
        filename = os.path.basename(escape(file.filename))
        file.save(os.path.join('uploads', filename))
        return 'File uploaded successfully'
    
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <input type="submit" value="Upload">
        </form>
    '''

# XSS 방지된 페이지
@app.route('/greet')
def greet():
    name = escape(request.args.get('name', ''))
    return f'<h1>Hello, {name}!</h1>'

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
