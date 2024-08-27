from flask import Flask, request, render_template, send_file
import sqlite3
import os

app = Flask(__name__)

# 취약점 1: SQL 인젝션
@app.route('/user/<username>')
def show_user_profile(username):
    # 사용자가 입력한 값을 그대로 SQL 쿼리에 사용
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return f'User: {user[0]}, Email: {user[1]}'
    else:
        return 'User not found', 404

# 취약점 2: 경로 탐색 (Path Traversal)
@app.route('/file/<path:filename>')
def get_file(filename):
    # 입력된 파일명을 그대로 경로로 사용
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return 'File not found', 404

# 취약점 3: 입력 데이터 검증 부족
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    return 'File uploaded successfully'

# 취약점 4: XSS (Cross-Site Scripting)
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', '')
    return f'<h1>Hello, {name}!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
