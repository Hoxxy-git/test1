import os
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, validators

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joleeus.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
db = SQLAlchemy(app)

# CSRF 보호 활성화
csrf = CSRFProtect(app)

# 사용자 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# 사용자 입력 폼
class UserForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=1, max=80)])

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return 'User added successfully!'
    
    return render_template_string('''
        <form method="post">
            {{ form.hidden_tag() }}
            Name: {{ form.name(size=20) }}
            <input type="submit" value="Add User">
        </form>
    ''', form=form)

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template_string('''
        <h1>Users</h1>
        <ul>
            {% for user in users %}
                <li>{{ user.name }}</li>
            {% endfor %}
        </ul>
    ''', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)