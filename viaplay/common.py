import logging
import os

logger = logging.getLogger(__name__)

# UPLOAD FILES FOR THE PROCEDURES
####################################################
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'procedures')
ALLOWED_EXTENSIONS = set(['py'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
