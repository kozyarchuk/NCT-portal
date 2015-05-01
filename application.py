import flask
from flask.templating import render_template
from flask import Flask, render_template, jsonify, request
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
import boto.sqs
from boto.sqs.message import Message
import boto
import random
import os
import dateutil.parser

application = flask.Flask(__name__)
application.secret_key = 'Secret'
BUCKET = 'nct-data'


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


class FilesForm(Form):
    file_name = StringField('file_name', validators=[DataRequired()])


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
    if request.method == 'GET':
        bucket = conn.s3.get_bucket(BUCKET)

        s3_files = [ FileRecord(key) for key in bucket.list() ]

        form = FilesForm()
        return render_template('files.html', form=form, files=sorted(s3_files, reverse=True))
    else:
        bucket = conn.s3.get_bucket(BUCKET)
        key = bucket.new_key('File%s' % random.random())
        key.set_contents_from_string('Hello World!')

        return "Message Sent"


if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
