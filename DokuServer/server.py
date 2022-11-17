import flask

# Create the application.
APP = flask.Flask(__name__)
APP.config['TEMPLATES_AUTO_RELOAD'] = True

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('README.html')


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=80)