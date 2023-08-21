from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main.html')


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
