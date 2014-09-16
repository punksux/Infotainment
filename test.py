__author__ = 'Chris'
#import gevent
#import gevent.monkey
#from gevent.pywsgi import WSGIServer
import time
#gevent.monkey.patch_all()
import random

from flask import Flask, request, Response, render_template

app = Flask(__name__)


def event_stream():
    i = 0
    while True:
        time.sleep(2)
        yield 'data: ' + (str(random.randrange(32, 104)) + '.' + str(random.randrange(0, 9))) + '\n\n' + \
        'event: count\n' + \
        'data: ' + str(i) + '\n\n'
        i += 1


@app.route('/my_event_source')
def sse_request():
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=801)
