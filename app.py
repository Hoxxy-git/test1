from flask import Flask, request, render_template_string
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

# XSS 취약점이 있는 페이지  
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return f'<h1>Hello, {name}!</h1>'

# 파일 업로드 취약점이 있는 페이지
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    return 'File uploaded successfully'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
