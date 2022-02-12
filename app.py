from flask import Flask, render_template, request, send_from_directory, make_response
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import os
from config import Config
from ml import process_file
import json

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['get', 'post'])
def index(filename=''):
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    img_list = request.cookies.get('img_list') or json.dumps([])
    img_list = json.loads(img_list)

    img_out_filename = ''
    if request.method == 'POST':
        file = request.files['img_file']
        if file and is_allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_')
            new_filename = timestamp + uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1]
            new_filename = secure_filename(new_filename.lower())
            file.save(os.path.join(app.config['IMG_UPLOAD_FOLDER'], new_filename))
            confidence = float(request.form.get('confidence'))
            img_out_filename = process_file(app, new_filename, confidence)
            while len(img_list) + 1 > app.config['MAX_CAROUSEL_IMAGES']:
                del (img_list[0])
            img_list.append(img_out_filename)

    resp = make_response(render_template('index.html',
                         img_out_filename=img_out_filename,
                         img_list=img_list[::-1],
                         max_coursel = app.config['MAX_CAROUSEL_IMAGES']))
    resp.set_cookie('img_list', json.dumps(img_list))
    return resp



@app.route("/img/out/<filename>")
def send_img(filename):
    return send_from_directory('data/img_out', filename)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
