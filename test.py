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
    while True:
        time.sleep(1)
        yield 'data: %s\n\n' % random.randrange(0,3000)

@app.route('/my_event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=801, debug=True)

