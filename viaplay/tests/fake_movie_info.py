from flask import Flask

app = Flask(__name__)


@app.route('/pc-se/film/ted-2-2015')
def imdb_info():
    return '_embedded["viaplay:blocks"][0]._embedded["viaplay:product"].content.imdb:"tt0137523"', 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9090)
