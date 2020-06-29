from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    title = 'Hello Fucking World!'
    # TODO: сделать конфигом
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'shovon.jpg')
    full_filename = os.path.join('static', '8.jpg')
    return render_template('index.html', title=title, h1=full_filename, user_image=full_filename)


# @app.route('/')
@app.route('/test_page')
def test_page():
    user = {'username': 'BANDIT'}
    return render_template('test_page.html', title='Home', user=user)


if __name__ == '__main__':
    app.run()
