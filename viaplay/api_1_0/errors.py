import logging

from werkzeug.exceptions import Conflict, NotFound

logger = logging.getLogger(__name__)


# RAISE ERRORS
##################################################################
def raise_exception(e, msg):
    description = getattr(e, 'description', repr(e))
    e.description = description
    e.message = msg
    raise e


def error_if_exists(name, coll, class_name):
    result = coll.find_one({"name": name})

    if result is not None:
        msg = "%s for name %r already exits" % (class_name, name)
        logger.error("Ups, there was an exception %r", msg)
        e = Conflict(description=msg)
        raise e


def error_if_not_found(result, name, class_name):
    if result is None:
        msg = "%s for name %r not found" % (class_name, name)
        logger.error("Ups, there was an exception %r", msg)
        e = NotFound(description=msg)
        raise e


def error_if_missing_keys(required_keys, arguments):
    keys = arguments.keys()

    if not all(k in keys and arguments[k] is not None for k in required_keys):
        missing_keys = [k for k in required_keys if k not in keys or arguments[k] is None]
        msg = "Not all required keys are provided. Missing: %r" % missing_keys
        logger.error(msg)
        e = Conflict(description=msg)
        raise e


def error_if_args_not_match(identifier, name):
    if name != identifier:
        msg = "name in url %r and name in arg %r are not the same." % (name, identifier)
        raise Conflict(description=msg)
