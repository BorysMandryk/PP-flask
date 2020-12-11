from wsgiref.simple_server import make_server
from flask import Flask


app = Flask(__name__)


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello world 15"


with make_server('', 8000, app) as server:
    server.serve_forever()


if __name__ == "__main__":
    app.run()
