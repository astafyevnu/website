# This Python file uses the following encoding: utf-8
from datetime import datetime, timedelta

from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify
from flask_wtf import CSRFProtect

from forms import LoginForm, RegistrationForm
from models import db, User, Review

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f66dfa7124da9bc2b6da3b5a169f0cdd2e6c9625e808138ebd00d711274463bf'
csrf = CSRFProtect(app)


@app.route('/form', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return 'No CSRF protection'


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
    ...
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


# В этом примере создается новый объект модели User с именем пользователя "john"
# и электронной почтой "john@example.com". Затем объект добавляется в сессию
# базы данных и сохраняется с помощью метода commit().
# @app.cli.command("add-john")
# def add_user():
#     user = User(username='john', email='john@example.com')
#     db.session.add(user)
#     db.session.commit()
#     print('John add in DB!')


# В этом примере получаем объект модели User по имени пользователя "john",
# изменяем его электронную почту на "new_email@example.com" и сохраняем
# изменения с помощью метода commit().
# @app.cli.command("edit-john")
# def edit_user():
#     user = User.query.filter_by(username='john').first()
#     user.email = 'new_email@example.com'
#     db.session.commit()
#     print('Edit John mail in DB!')

# В этом примере получаем объект модели User по имени пользователя "john",
# удаляем его из базы данных с помощью метода delete() и сохраняем изменения с
# помощью метода commit().
# @app.cli.command("del-john")
# def del_user():
#     user = User.query.filter_by(username='john').first()
#     db.session.delete(user)
#     db.session.commit()
#     print('Delete John from DB!')

# Вначале мы записываем в БД count пользователей. А далее генерируем статье,
# которые они написали.
@app.cli.command("fill-db")
def fill_tables():
    count = 5
    # Добавляем пользователей
    for user in range(1, count + 1):
        new_user = User(username=f'user{user}',
                        email=f'user{user}@mail.ru')
        db.session.add(new_user)
        db.session.commit()

    #     # Добавляем статьи
    for review in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{review % count + 1}').first()
        new_review = Review(title=f'Review title {review}',
                            content=f'Review content {review}', author=author)
        db.session.add(new_review)
        db.session.commit()


# Для получения данных из базы данных необходимо использовать метод query()
# модели. Этот метод возвращает объект запроса, который можно дополнить
# фильтрами и другими параметрами.
@app.route('/users//')
def all_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


@app.route('/users/<username>/')
def users_by_username(username):
    users = User.query.filter(User.username == username).all()
    context = {'users': users}
    return render_template('users.html', **context)


@app.route('/reviews/author/<int:user_id>/')
def get_reviews_by_author(user_id):
    reviews = Review.query.filter_by(author_id=user_id).all()
    if reviews:
        return jsonify([{'id': review.id, 'title': review.title,
                         'content': review.content, 'created_at': review.created_at} for review
                        in reviews])
    else:
        return jsonify({'error': 'Reviews not found'})


@app.route('/reviews/last-week/')
def get_reviews_last_week():
    date = datetime.utcnow() - timedelta(days=7)

    reviews = Review.query.filter(Review.created_at >= date).all()
    if reviews:
        return jsonify([{'id': review.id, 'title': review.title,
                         'content': review.content, 'created_at': reviews.created_at} for review
                        in reviews])
    else:
        return jsonify({'error': 'Reviews not found'})


@app.route('/feedback//', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        response = make_response(redirect(url_for('us_answer_page')))
        response.set_cookie('name', name)
        response.set_cookie('email', email)
        response.set_cookie('message', message)
        return response
    return render_template('feedback.html')


@app.route('/us_answer/', methods=['POST', 'GET'])
def us_answer_page():
    if request.method == 'POST' and request.form.get('quit'):
        response = make_response(redirect(url_for('feedback_page')))
        response.set_cookie('name', max_age=0)
        response.set_cookie('email', max_age=0)
        response.set_cookie('message', max_age=0)
        return response

    context = {
        'name': request.cookies.get('name')
    }
    return render_template('us_answer.html', **context)


# @app.route('/login//', methods=['GET', 'POST'])
# def login_page():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         response = make_response(redirect(url_for('greeting_page')))
#         response.set_cookie('email', email)
#         response.set_cookie('password', password)
#         return response
#     return render_template('login.html')


@app.route('/greeting/', methods=['POST', 'GET'])
def greeting_page():
    if request.method == 'POST' and request.form.get('quit'):
        response = make_response(redirect(url_for('login_page')))
        response.set_cookie('email', max_age=0)
        response.set_cookie('password', max_age=0)
        return response

    context = {
        'email': request.cookies.get('email')
    }
    return render_template('greeting.html', **context)


@app.route('/clothes//')
def clothes_page():
    return render_template('clothes.html')


@app.route('/shoes//')
def shoes_page():
    return render_template('shoes.html')


@app.route('/hats//')
def hats_page():
    return render_template('hats.html')


@app.route('/accessories//')
def accessories_page():
    return render_template('accessories.html')


@app.route('/about_us//')
def about_us_page():
    return render_template('about_us.html')


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


if __name__ == "__main__":
    app.run(debug=True)
