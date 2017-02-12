import logging
import json
import re

from flask import Blueprint, jsonify, current_app, request
from flask_restful import Api, Resource
from werkzeug.exceptions import Conflict, NotFound

from .errors import raise_exception

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


class viaplayApi(Api):
    """ Override the API to handle custom errors """

    def handle_error(self, e):
        try:
            logger.exception("viaplayApi captured exception")
            code = getattr(e, 'code', 500)
            description = getattr(e, 'description', None)
            message = getattr(e, 'message', None)
            description = description or message
            json_dict = {"status": code}

            if message:
                json_dict['message'] = message

            if description:
                json_dict['description'] = description

            if hasattr(e, 'json'):
                json_dict['additionalInfo'] = e.json

            return jsonify(json_dict), code

        except Exception as e:
            msg = "This is embarasing... there was an error handling the error"
            json_dict = {"status": 500, "message": msg}

            if hasattr(e, description):
                json_dict['additionalInfo'] = e.description

            return jsonify(json_dict), 500


class viaplay(Resource):

    def get(self, action=None, url=None):
        """ From the given URL find the IMDB information, then from TMDB find the trailer URL and return

        :statuscode 200: response with trailer URL
        :statuscode 404: resource not found
        :statuscode 500: internal server error
        """

        def find(config=None, url=None):
            import requests

            # get the input URL information
            logger.debug("Get movie resource URL: %s", url)

            if(url is not None and check_url(config, url)):
                try:
                    response = requests.get(url, timeout=config['TIMEOUT'])

                except Exception as e:
                    logger.error("can not get imdb information from the input URL!")
                    return e

                split_string = config['PATH_TO_IMDBINFO']

                # Assume there's only one IMDB id in the movie resource return value
                imdb_id_raw = response.text.split(split_string, 1)[1]
                p = re.compile('(tt|nm|ch|co|ev)\d+')
                m = p.search(imdb_id_raw)

                if m:
                    imdb_id = m.group(0)
                else:
                    msg = "Invalid IMDB ID found! %s" % imdb_id_raw
                    e = Conflict(description=msg)
                    raise_exception(e, msg)

                logger.info("IMDB id is: %s", imdb_id)

                fetch_trailer_url = (config['TRAILER_FETCHER'] +
                                     imdb_id +
                                     '/videos?api_key=' +
                                     config['TMDB_KEY'] +
                                     '&&language=' +
                                     config['PREFERED_LANGUAGE'])

                try:
                    trailer_response = requests.get(fetch_trailer_url, timeout=config['TIMEOUT'])

                except Exception as e:
                    logger.error("can not get trailer url! %s", fetch_trailer_url)
                    return e

                trailer_info = json.loads(trailer_response.text)

                trailer_urls = []
                for trailer in trailer_info["results"]:
                    logger.debug("Found trailer %s on site %s for movie %s" %
                                 (trailer["key"], trailer["site"], imdb_id))

                    youtube_trailer_url = 'https://www.youtube.com/watch?v=' + trailer["key"]
                    trailer_urls.append(youtube_trailer_url)

                return trailer_urls

            else:
                logger.error("Invalid movie resource URL!: %s", url)

                msg = "Invalid URL provided! %s" % url
                e = Conflict(description=msg)
                raise_exception(e, msg)

        def check_url(config=None, url=None):
            """ check if the url is valid or not.
                should only allow the url pointing to under https://content.viaplay.se/pc-se/film/
            """

            for valid_url in config['VALID_URL_LIST']:
                p = re.compile(valid_url)
                logger.debug("validating the input URL: %s", url)
                m = p.match(url)

                if m:
                    logger.debug("The input URL: %s is valid", url)
                    return True

            logger.debug("The input URL: %s is invalid", url)
            return False

        actions = {"find": find}

        config = current_app.config
        url = request.args.get('url')

        if action and action not in actions:
            e = NotFound(description='action {} not available'.format(action))
            msg = "error at viaplay fetcher"
            raise_exception(e, msg)

        action = action or "find"

        logger.debug("Get url %s from input", url)

        return jsonify(actions[action](config, url))

api = viaplayApi(api_bp, catch_all_404s=True)

api.add_resource(viaplay, '/', '/<string:action>')
