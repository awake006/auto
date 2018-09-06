from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def get_json():
    data = {'name': 'xiaoming', 'age': 18}
    return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
