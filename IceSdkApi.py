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

@app.errorhandler(413)
def too_large(e):
    return jsonify(success=False, message='Bad request: File is too large')

@app.route("/")
def hello_world():
    return "Usage: curl -F 'files=@pathToSoFile -F 'files=@pathToSigFile' http://localhost:5000/upload"

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if not UPLOAD_FOLDER.is_dir():
        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    app.logger.info('Upload file')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            app.logger.info('Bad request: missing files part')
            return jsonify(success=False, message='Bad request: missing files part: please attach one .so and one .sig files as parameter')

        files = request.files.getlist('files')
        newFiles={}
        for file in files:
            result = upload_file(file)
            if not result['success']:
                return jsonify(success=False, message=result['message'])
            newFiles[file]=result['file']

        for reqFile, newFile in newFiles.items():
            reqFile.save(newFile)
        
        resp = jsonify(success=True, message=f'File(s) successfully uploaded')
        resp.status_code = 200
        return resp
        
    return jsonify(success=False, message='Bad request: request method should be POST')

def upload_file(file):
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
            app.logger.info('Bad request: no selected file')
            return dict(success=False, message='Bad request: no selected file, the file part in the request is present, but empty.')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        app.logger.info('Uploading %s', filename)
        newFile=app.config['UPLOAD_FOLDER'].joinpath(filename)
        if newFile.is_file():
            return dict(success=False, message=f'File "{filename}" already exists.')

        return dict(success=True, file=newFile, filename = filename)

    return jsonify(success=False, message='Bad request: only .so and .sig extensions are allowed')


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
    ALLOWED_EXTENSIONS = {'so', 'sig'}
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.use_reloader = False

    args = setup_args()
    UPLOAD_FOLDER = Path(args.workspace)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    setup_logger()

    app.run(host='0.0.0.0', debug=True)
