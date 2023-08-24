from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main.html')


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


@app.route('/login//', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = make_response(redirect(url_for('greeting_page')))
        response.set_cookie('email', email)
        response.set_cookie('password', password)
        return response
    return render_template('login.html')


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


if __name__ == "__main__":
    app.run(debug=True)
