import flask
from flask import render_template, request, flash, redirect, url_for
from boto.sqs.message import Message
import boto
import time
import os
import dateutil.parser
from werkzeug import secure_filename


application = flask.Flask(__name__)
application.secret_key = 'Secret'
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

BUCKET = 'nct-data'
ALLOWED_EXTENSIONS = set(['.txt', '.csv', '.xls', '.xlsx','.dat'])

class FileRecord:
    def __init__(self, key):
        self.name = key.name.decode("utf-8")
        self.size = key.size
        self.upload_time = key.last_modified

    def __cmp__(self, other):
        return cmp(self.upload_time, other.upload_time)

    @property
    def formatted_upload_time(self):
        d = dateutil.parser.parse(self.upload_time)
        return d.strftime("%B %d, %Y %I:%M%p")

class Conn:
    _s3 = None
    _sqs = None

    @property
    def s3(self):
        if not self._s3:
            self._s3 = boto.connect_s3()
        return self._s3

    @property
    def sqs(self):
        if not self._sqs:
            self._sqs = boto.sqs.connect_to_region("us-east-1")
        return self._sqs


conn = Conn()


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
    if request.method == 'POST':
        trade_file = request.files['trade_file']
        if trade_file :
            bucket = conn.s3.get_bucket(BUCKET)
            base_name, extension = os.path.splitext( secure_filename( trade_file.filename ) )
            if extension in ALLOWED_EXTENSIONS:
                file_name = "%s.%s.%s" % (base_name, time.time(),extension)
                key = bucket.new_key(file_name)
                key.set_contents_from_string(trade_file.stream.read())
                flash("File Saved",'info')
            else:
                flash("Unsupported extension %s. Only %s are supported" % (extension, ALLOWED_EXTENSIONS),'error')
        else:
            flash("File is missing",'error')
        return redirect('/files.html')
    else:
        bucket = conn.s3.get_bucket(BUCKET)
        ordered_list = sorted(bucket.list(), key=lambda k: k.last_modified)
        s3_files = [ FileRecord(key) for key in ordered_list[0:20] ]
        return render_template('files.html', files=sorted(s3_files, reverse=True))

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
