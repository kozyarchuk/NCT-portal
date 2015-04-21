import flask
from flask.templating import render_template

application = flask.Flask(__name__)

@application.route('/')
@application.route('/index.html')
def hello_world():
    return render_template('index.html', name="Travis-CI")

if __name__ == '__main__':
    application.debug=True
    application.run(host='0.0.0.0')
