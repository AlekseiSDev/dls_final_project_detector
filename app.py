import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from model_api import model
import PIL
import cv2

# import request
UPLOAD_FOLDER = os.path.join('static', 'uploads')
UPLOADS_ABS_PATH = join(dirname(realpath(__file__)), UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['in_folder'] = 'static'
app.config['out_folder'] = os.path.join('static', 'out')

app.config['in_img'] = os.path.join('static', 'original_picture_1.jpg')
app.config['out_img'] = os.path.join('static', 'picture_with_bb_1.jpg')

model = model()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    """

    :return:
    """
    title = 'Hello Fucking World!'
    # in_img = os.path.join('static', 'original_picture_1.jpg')
    # out_img = os.path.join('static', 'picture_with_bb_1.jpg')
    if request.method == 'POST':
        if request.form['submit_button'] == 'Upload':
            file = request.files['file']
            if file and __allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # TODO: рот ебал этих путей
                in_app_path = os.path.join(UPLOAD_FOLDER, filename)
                save_path = os.path.join(UPLOADS_ABS_PATH, filename)

                file.save(save_path)
                app.config['in_img'] = in_app_path
        elif request.form['submit_button'] == 'process_picture':
            in_abs_file = join(dirname(realpath(__file__)), app.config['in_img'])
            out_abs_file = join(dirname(realpath(__file__)), app.config['out_folder'], 'out.jpg')
            process_img(in_abs_file, out_abs_file)
            app.config['out_img'] = os.path.join('static', 'out', 'out.jpg')
    return render_template('index.html', title=title, picture_original=app.config['in_img'],
                           picture_with_bb=app.config['out_img'])


# @app.route('/')
@app.route('/test_page')
def test_page():
    user = {'username': 'BANDIT'}
    return render_template('test_page.html', title='Home', user=user)


# TODO: обработка изображения, пока заглашука
def process_img(img_path, out_path):
    #TODO: чтение изображения в cv и PIL форматах

    image_pil= PIL.Image.open(img_path)
    img_cv = cv2.imread(img_path)

    output = model.get_predict(image_pil, img_cv)

    cv2.imwrite(out_path, output)
    return out_path


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
