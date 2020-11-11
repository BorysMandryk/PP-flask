from flask import Flask


app = Flask(__name__)


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello world 15"


if __name__ == "__main__":
    app.run()