import flask
from flask.templating import render_template
from flask import Flask, render_template, jsonify, request
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
import boto.sqs
from boto.sqs.message import Message

application = flask.Flask(__name__)
application.secret_key = 'Secret'

_boto_conn = None
def get_boto_conn():
    global _boto_conn
    if not _boto_conn:
        _boto_conn = boto.sqs.connect_to_region("us-east-1")

    return  _boto_conn

class FilesForm(Form):
    file_name = StringField('file_name', validators=[DataRequired()])

@application.route('/')
@application.route('/index.html')
def index():
    return render_template('index.html' )


@application.route('/files.html', methods=['GET', 'POST'])
def files():
    if request.method == 'GET':
        form = FilesForm()
        return render_template('files.html', form=form)
    else:
        conn = get_boto_conn()
        q = conn.get_queue('NCT-service-request')
        m = Message()
        m.set_body('The file is on its way.')
        q.write(m)
        return "Message Sent"

if __name__ == '__main__':
    application.debug=True
    application.run(host='0.0.0.0')
