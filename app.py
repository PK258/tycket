import os
import time

from flask import Flask, flash, request, redirect, render_template
from flask_bootstrap import Bootstrap

import uploadtycket
import config

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_url_path='', static_folder='static',
            template_folder=config.template_folder)
Bootstrap(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename):
    filename, extension = os.path.splitext(filename)
    return extension


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            ext = file_extension(file.filename)
            filename = uploadtycket.filename(time.time())
            img = file.read()
            url = uploadtycket.upload_file(img, '/Tycket-images/' + filename + ext)
            result = {
                'class_name': filename,
                'image_path': url,
            }
            uploadtycket.update_google_sheet(filename, url)
            # return render_template('result.html', result=result)
            return os.path.join(os.getcwd(), 'tycket/templates')
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
