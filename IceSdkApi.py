# import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from argparse import ArgumentParser

# app.secret_key = "secret key"
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not UPLOAD_FOLDER.is_dir():
        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    app.logger.info('Upload file')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.info('No file part')
            return jsonify(success=False, message='No file part in the request, please give a file as parameter')

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            app.logger.info('No selected file')
            return jsonify(success=False, message='No selected file, the file part in the request is present, but empty.')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info('Uploading %s', filename)
            new_file=app.config['UPLOAD_FOLDER'].joinpath(filename)
            if new_file.is_file():
                return jsonify(success=False, message='File already exists.')

            file.save(new_file)
            resp = jsonify(success=True, message=f'{filename} successfuly uploaded.')
            resp.status_code = 200
            return resp

    return jsonify(success=False)
 

# Logging only for the PoC version
# @app.before_first_request
# def before_first_request():
#     log_level = logging.INFO

#     for handler in app.logger.handlers:
#         app.logger.removeHandler(handler)

#     root = os.path.dirname(os.path.abspath(__file__))
#     logdir = os.path.join(root, 'logs')
#     if not os.path.exists(logdir):
#         os.mkdir(logdir)

#     log_file = os.path.join(logdir, 'app.log')
#     handler = logging.FileHandler(log_file)
#     handler.setLevel(log_level)
#     app.logger.addHandler(handler)
#     app.logger.setLevel(log_level)
 

def setup_logger():
  MAX_BYTES = 10e6 # Maximum size for a log file
  BACKUP_COUNT = 9 # Maximum number of old log files

  log_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(log_format)
  stream_handler.setLevel(logging.INFO)

  app.logger.addHandler(stream_handler)

  p = Path.cwd().joinpath(Path('logs'))
  p.mkdir(parents=True, exist_ok=True)

  log_file=p.joinpath('app.log')

  file_handler = RotatingFileHandler(log_file, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
  file_handler.setFormatter(log_format)
  file_handler.setLevel(logging.INFO)

  app.logger.addHandler(file_handler)
  app.logger.setLevel(logging.INFO)

def setup_args():
    parser = ArgumentParser(description='Arguments for ICE-SDK file uploader RestAPI')
    parser.add_argument('-w', '--workspace',
                        required=True,
                        action='store',
                        help='Destination directory where the uploaded files are going to be stored.')
    my_args = parser.parse_args()

    return my_args

if __name__ == "__main__":
    #UPLOAD_FOLDER = Path('/data/plugins_2')
    ALLOWED_EXTENSIONS = {'so'}
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.use_reloader = False

    args = setup_args()
    UPLOAD_FOLDER = Path(args.workspace)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    setup_logger()

    app.run(host='0.0.0.0', debug=True)
