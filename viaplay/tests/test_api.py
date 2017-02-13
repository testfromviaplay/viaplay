import json
import re
from flask import url_for
from viaplay import create_app, version
from nose.tools import *


def test_correct_url():
    app = create_app('default')
    app_context = app.app_context()
    app_context.push()
    client = app.test_client()
    response = client.get('http://127.0.0.1:5951/api/v1.0/find?url=http://localhost:9090/pc-se/film/ted-2-2015')
    eq_(b"200 OK", response.status)
