from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)


@app.route('/poo', methods=['POST'])
def add_numbers():
    print(request.form.get('a', 0, type=int))
    print(request.form.get('b', 0, type=int))
    a = request.form.get('a', 0, type=int)
    b = request.form.get('b', 0, type=int)
    result = a + b
    return jsonify({'1': result})

@app.route('/')
def page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=801)
