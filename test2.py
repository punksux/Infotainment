from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)


@app.route('/weather.json', methods=['GET'])
def sse_request():
    return jsonify({'weather': 'cloudy', 'temp': '75'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)