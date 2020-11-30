from backend.app import app
from libs.src.download_manager import DownloadManger
from flask import request, abort, jsonify
import os
from werkzeug.utils import secure_filename

UPLOAD_DIRECTORY = "/home/local/Downloads/input"

ALLOWED_EXTENSIONS = ['zip']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/fileupload', methods=['POST'])
def upload_file():
    upload_file_path = None

    # check if the post request has the file part
    if 'filename' not in request.files:
        resp = jsonify({'message' : 'No file part in the request...'})
        resp.status_code = 400
        return resp

    file = request.files['filename']

    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(upload_file_path)
        resp = jsonify({'message' : 'File successfully uploaded.'})
        resp.status_code = 201

        dm = DownloadManger()
        dm.upload_file(upload_file_path)
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are zip'})
        resp.status_code = 400
        return resp

# curl --request PUT --upload-file CSVFiles.zip https://dev-s3-datastax.s3.amazonaws.com/
@app.route('/api/presigned')
def pre_signed_url():
    object_name = "CSVFiles.zip"

    dm = DownloadManger()
    return dm.create_presigned_post(object_name)



