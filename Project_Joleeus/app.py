from flask import Flask, request, redirect, url_for, render_template_string
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

# SQL Injection 취약점이 있는 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # SQL Injection 취약점이 있는 코드
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return f'Welcome, {username}!'
        else:
            return 'Invalid credentials!'

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# 파일 업로드 취약점이 있는 페이지 (Path Traversal)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename  # 이 코드에는 Path Traversal 취약점이 존재합니다.
        file.save(os.path.join('uploads', filename))
        return 'File uploaded successfully'
    
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <input type="submit" value="Upload">
        </form>
    '''

# XSS 취약점이 있는 페이지
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return f'<h1>Hello, {name}!</h1>'  # 이 코드에는 XSS 취약점이 존재합니다.

if __name__ == '__main__':
    init_db()  # 데이터베이스 초기화
    app.run(debug=True)  # 애플리케이션 실행
