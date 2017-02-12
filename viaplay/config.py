import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Set the http request timeout. default is 20ms
    TIMEOUT = 0.02
    UPLOAD_FOLDER = "procedures/"

    # The URL allowed to get IMDB information
    VALID_URL_LIST = ["https://content.viaplay.se/pc-se/film/", "http://127.0.0.1:9090/"]

    # The path where to find IMDB information
    PATH_TO_IMDBINFO = "_embedded[\"viaplay:blocks\"][0]._embedded[\"viaplay:product\"].content.imdb:"

    # The Key to access TMDB
    TMDB_KEY = "e2c169ebf96ff0ca4ee06425fa38a941"

    # The API to get trailer URL. currently using TMDB, API V3
    TRAILER_FETCHER = "https://api.themoviedb.org/3/movie/"

    # Prefered trailer language
    PREFERED_LANGUAGE = "en-US"

    @staticmethod
    def init_app(app):
        pass


class ConfigFile(Config):
    """ This class reads the configuration from a file """
    CONFIG_FILE = os.environ.get("CONFIG_FILE", "/etc/viaplay.json")
    " A default configuration file should be at /etc/viaplay.json "

    @staticmethod
    def init_app(app):
        """ Load the file only when the class is used """
        import json
        with open(ConfigFile.CONFIG_FILE) as json_file:
            json_data = json.load(json_file)

        app.config.update(json_data)


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'environment': Config,
    'development': DevelopmentConfig,
    'file': ConfigFile,
    'default': ConfigFile
}
