from distutils.log import debug
import os
import logging
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'so'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    app.logger.info('Upload file')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            app.logger.info('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            app.logger.info('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info('%s file_to_upload', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify(success=True)
            resp.status_code = 200
            return resp
    return jsonify(success=False)
    

@app.before_first_request
def before_first_request():
    log_level = logging.INFO
 
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
 
    app.logger.setLevel(log_level)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    # app.logger.info('App init')
