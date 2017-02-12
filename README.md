# Viaplay test project

This API is built using flask and gevent WSGI server. 

When the API start, it will listen on a configured port, any http get request to this port will be validated. If the request point to an allowed website and contains a valid movie infor request, the request will be send to the allowed website. The API expect to receive a valid IMDB id from this request

If the IMDB id is valid, this API will try to use this IMDB and get available youtube trailer URL from TMDB site

## Installation

    sudo apt install python-pip
    pip install virtualenv
    git clone https://github.com/testfromviaplay/viaplay.git
    virtualenv venv
    source venv/bin/activate
    pip install -e viaplay/
    sudo cp viaplay/viaplay.json /etc/

## Usage

    start viaplay-api
    sudo bash
    source venv/bin/activate
    viaplay-api

## Testing

   1. start the fake movie info website
        cd viaplay/viaplay/tests/
        ./start_fake.sh
    
   2. send some curl command to the viaplay-api, to verify it can handle the URL it get, or genereate correct exception
        curl -X GET 'http://127.0.0.1:5951/api/v1.0/find?url=http://localhost:9090/pc-se/film/ted-2-2015'

## Configuration

When start the api, configuration file /etc/viaplay.json will be read. 

    "TRAILER_GET_SERVER_PORT": 5951,    ## the port viaplay-api will listen to
    "TIMEOUT": 2,                       ## the timeout for all requests.get action 
    "UPLOAD_FOLDER":  "procedures/",
    "VALID_URL_LIST": ["https://content.viaplay.se/pc-se/film/", "http://localhost:9090/"],  ## allowed url list to get movie info
    "PATH_TO_IMDBINFO": "_embedded[\"viaplay:blocks\"][0]._embedded[\"viaplay:product\"].content.imdb:",  ## the header to be removed in the returned movie info
    "TMDB_KEY": "e2c169ebf96ff0ca4ee06425fa38a941",    ## the api key will be used to access tmdb website
    "TRAILER_FETCHER": "https://api.themoviedb.org/3/movie/",  ## the api will use api v3 from tmdb website, "get movie" api
    "PREFERED_LANGUAGE": "en-US"

## Reason of why build the API in current way

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
