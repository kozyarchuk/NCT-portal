import flask
from flask.templating import render_template
from flask import Flask, render_template, jsonify, request
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
import boto.sqs
from boto.sqs.message import Message
import boto
import  random

application = flask.Flask(__name__)
application.secret_key = 'Secret'
BUCKET = 'nct-data'

class Conn:
    _s3 = None
    _sqs = None

    @property
    def s3(self):
        if not self._s3:
            self._s3 = boto.connect_s3()
        return  self._s3

    @property
    def sqs(self):
        if not self._sqs:
            self._sqs = boto.sqs.connect_to_region("us-east-1")
        return  self._sqs

conn = Conn()

class FilesForm(Form):
    file_name = StringField('file_name', validators=[DataRequired()])

@application.route('/')
@application.route('/index.html')
def index():
    return render_template('index.html' )


@application.route('/files.html', methods=['GET', 'POST'])
def files():
    try:
        if request.method == 'GET':
            bucket = conn.s3.get_bucket(BUCKET)
            s3_files = []
            for key in bucket.list():
                s3_files.append("{name}\t{size}\t{modified}".format(
                    name = key.name, size = key.size,
                    modified = key.last_modified ))

            form = FilesForm()
            return render_template('files.html', form=form, files = s3_files)
        else:
            # q = conn.sqs.get_queue('NCT-service-request')
            # m = Message()
            # m.set_body('The file is on its way.')
            # q.write(m)

            bucket = conn.s3.get_bucket(BUCKET)
            key = bucket.new_key('File%s'% random.random())
            key.set_contents_from_string('Hello World!')


            return "Message Sent"
    except:
        import  traceback
        return  traceback.format_exc()

if __name__ == '__main__':
    application.debug=True
    application.run(host='0.0.0.0')
