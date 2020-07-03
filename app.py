import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# import request
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['in_img'] = os.path.join('static', 'original_picture_1.jpg')
app.config['out_img'] = os.path.join('static', 'picture_with_bb_1.jpg')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    """

    :return:
    """
    title = 'Hello Fucking World!'

    if request.method == 'POST':
        if request.form['submit_button'] == 'Upload':
            file = request.files['file']
            if file and __allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                app.config['in_img'] = save_path
        elif request.form['submit_button'] == 'process_picture':
            app.config['out_img'] = process_img(app.config['in_img'])
    return render_template('index.html', title=title, picture_original=app.config['in_img'],
                           picture_with_bb=app.config['out_img'])


# @app.route('/')
@app.route('/test_page')
def test_page():
    user = {'username': 'BANDIT'}
    return render_template('test_page.html', title='Home', user=user)


# TODO: обработка изображения, пока заглашука
def process_img(img_path):
    return img_path


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
