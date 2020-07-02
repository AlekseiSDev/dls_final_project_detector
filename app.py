import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# import request
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    """

    :return:
    """
    title = 'Hello Fucking World!'
    # TODO: сделать конфигом
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'shovon.jpg')
    in_img = os.path.join('static', 'original_picture_1.jpg')
    out_img = os.path.join('static', 'picture_with_bb_1.jpg')

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO: перестроить входное изображение
            in_img = save_path
            out_img = process_img(in_img)
    return render_template('index.html', title=title, picture_original=in_img, picture_with_bb=out_img)


# @app.route('/')
@app.route('/test_page')
def test_page():
    user = {'username': 'BANDIT'}
    return render_template('test_page.html', title='Home', user=user)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO: обработка изображения, пока заглашука
def process_img(img_path):
    return img_path


if __name__ == '__main__':
    app.run()
