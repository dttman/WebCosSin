from flask import Blueprint, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
from Config import Config

upload_route = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@upload_route.route('/upload', methods=['GET', 'POST'])
# Роут для загрузки изображения(промежуточный). После загрузки переходит к странице результата
def upload():
    if request.method == 'POST':
        file = request.files['file']
        funcSC=request.form.get('SINCOS')
        znach_func=request.form.get('znachSINCOS')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            return redirect(f"/result/{filename}/{funcSC}/{znach_func}")
        else:
            return redirect(f"/result")
