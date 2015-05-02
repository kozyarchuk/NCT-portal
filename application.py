import flask
from flask import render_template, request, flash, redirect, url_for
from gateway import s3
from domain.file_record import FileRecord
import os

application = flask.Flask(__name__)
application.secret_key = os.environ['SECRET_KEY']

application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.route('/')
@application.route('/index.html')
def index():
    return render_template('index.html')

@application.route('/analyze.html')
@application.route('/secmaster.html')
def under_construction():
    return render_template('under_construction.html')

@application.route('/files.html', methods=['GET', 'POST'])
def files():
    bucket = s3.gw.get_file_upload_bucket()
    if request.method == 'POST':
        message, status = FileRecord.upload_file(bucket, request.files['trade_file'])
        flash(message, status)
        return redirect('/files.html')
    else:
        return render_template('files.html', files=FileRecord.get_latest(bucket))

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
