# Viaplay test project

This API is built using flask and gevent WSGI server. Currently it's verified under Ubuntu 16.04 + Python 2.7 environment

When the API start, it will listen on a configured port, any http "get" request to this port will be validated. If the request point to an allowed website and contains a valid "movie info" request(the API expect to receive a valid IMDB id from this request), the request will be send to the allowed website. 

If the IMDB id is valid, this API will try to use this IMDB id and get available Youtube trailer URL from TMDB site

## Installation

    sudo apt install python-pip
    pip install virtualenv
    git clone https://github.com/testfromviaplay/viaplay.git
    virtualenv venv
    source venv/bin/activate
    pip install -e viaplay/
    sudo cp viaplay/viaplay.json /etc/

## Usage

    sudo bash
    source venv/bin/activate
    viaplay-api

## Testing

   1. start the fake "movie info" website
   
        cd viaplay/viaplay/tests/
        ./start_fake.sh
    
   2. send some curl command to the viaplay-api, to verify it can get trailer properly, or genereate proper exception. For example:
   
         curl -X GET 'http://127.0.0.1:5951/api/v1.0/find?url=http://localhost:9090/pc-se/film/ted-2-2015'

## Configuration

When start the API, configuration file /etc/viaplay.json will be read. 

    "TRAILER_GET_SERVER_PORT": 5951,    ## the port viaplay-api will listen to
    "TIMEOUT": 2,                       ## the timeout for all requests.get action 
    "UPLOAD_FOLDER":  "procedures/",
    "VALID_URL_LIST": ["https://content.viaplay.se/pc-se/film/", "http://localhost:9090/"],  ## allowed url list to get movie info
    "PATH_TO_IMDBINFO": "_embedded[\"viaplay:blocks\"][0]._embedded[\"viaplay:product\"].content.imdb:",  ## the header to be removed in the returned movie info
    "TMDB_KEY": "e2c169ebf96ff0ca4ee06425fa38a941",    ## the API key will be used to access tmdb website
    "TRAILER_FETCHER": "https://api.themoviedb.org/3/movie/",  ## using API v3 from tmdb website, "get movie" API
    "PREFERED_LANGUAGE": "en-US"

## Why build the API in current way

### choose of flask
I choose flask instead of Node.js mainly due to the exception handling. 2 years ago before I started to work with RESTful microframeworks, did some evaluation among several options at that time. The conclusion was if we want to have reasonable error handling "out of box", Node.js will be out of options.

There are some other reasons when choosing flask instead of other microframeworks:
  - light weight and meanwhile powerful enough
  - Blueprints make it very easy to expand the project in future
  - most widely used python microframework, means when some problem happenes during developing or integerating, the problem is most likely already be tagged by other users, and fixed or walk-arounded
  - almost painless when deploying with pip

### choose of gevent
Using gevent together with flask means requests to the service is almost "non-blocking", and it's very light weight.

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
