import os
import logging
import logging.config
import socket

from flask import Flask

from .config import config

from .common import UPLOAD_FOLDER

from gevent.wsgi import WSGIServer

logger = logging.getLogger(__name__)

##############################################################################
# LOGGING CONFIGURATION
# Check if there a configuration file

# Using default configuration for logging
strformat = ('[%(asctime)s] %(name)-20s %(filename)s:%(lineno)d ' +
             '%(levelname)s %(message)s')
logging.basicConfig(
    filename='/var/log/viaplay.log',
    level=logging.DEBUG,
    format=strformat,
    datefmt='%m/%d/%y %H:%M:%S')
logging.getLogger(__name__).setLevel(logging.DEBUG)

##############################################################################
# APP


def create_app(config_name='default'):
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'templates')
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api_1_0 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1.0')

    return app


def run(config_profile=None):  # pragma: no cover
    config_profile = os.getenv('VIAPLAY_CONFIG_FILE') or 'default'

    app = create_app(config_profile)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Read the configuraiton to change the port if necessary
    port = int(app.config['TRAILER_GET_SERVER_PORT'])

    logger.info(">>>> viaplay-trailer-fetcher >>>> Starting with %r profile." % (config_profile))

    # CONFIGURATION
    logger.info(">>>> viaplay-trailer-fetcher >>>> Configuration:")
    for k, v in app.config.items():
        logger.info("\t\t\t\t %s: %s" % (k, v))

    # Since we do not use any webserevr that serves the flask request
    # we listen to all the interfaces
    try:
        logger.info("Publish service at port:  %s" % (port))

        http_server = WSGIServer(('', port), app)
        http_server.serve_forever()

    except socket.error:
        logger.critical("Cannot start the server on http://0.0.0.0:{}. \
                         Check if the address is already in use".format(port))


def get_version():
    import pkg_resources  # part of setuptools
    return pkg_resources.require("viaplay")[0].version


def version():
    return get_version()
