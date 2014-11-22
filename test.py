import os
from time import sleep
from datetime import datetime, timedelta
import time
from apscheduler.scheduler import Scheduler
from flask import Flask, render_template, Response, request, jsonify
import random
import platform

on_pi = False

print("** Running on " + platform.uname()[0] + " **")
if platform.uname()[0] != 'Windows':
    on_pi = True

temp_sensor = '/sys/bus/w1/devices/28-0004749a3dff/w1_slave'

sched = Scheduler()
sched.start()

app = Flask(__name__)

if on_pi:
    import RPi.GPIO as GPIO
    os.system("sudo modprobe w1-gpio && sudo modprobe w1-therm")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, True)


def tempdata():
    global temp_mc
    if on_pi:
        y = open(temp_sensor, 'r')
        lines = y.readlines()
        y.close()

        if lines[0].strip()[-3:] != 'YES':
            print('No temp from sensor.')
            time.sleep(5)
            tempdata()
        else:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_mc = lines[1][equals_pos+2:]  # temp in milliCelcius
        return temp_mc
    else:
        return random.randint(0, 80)


def turn_on():
    if on_pi:
        GPIO.output(11, False)
    else:
        print('On')


def turn_off():
    if on_pi:
        GPIO.output(11, True)
    else:
        print('Off')

target = 30 * 1000
P = 6
I = 2
B = 22

# Initialise some variables for the control loop
interror = 0
pwr_cnt = 1
pwr_tot = 0

# Turn on for initial ramp up
state = "on"
turn_on()


def start_up():
    temperature = tempdata()
    print("Initial temperature ramp up")
    while target - temperature > 6000:
        sleep(15)
        temperature = tempdata()
        print(temperature)
    a = sched.add_date_job(control_loop, datetime.now() + timedelta(seconds=2))


def control_loop():
    print("Entering control loop")
    global interror, state
    while True:
        temperature = tempdata()
        print(temperature)
        error = target - temperature
        interror += error
        power = B + ((P * error) + ((I * interror) / 100)) / 100
        print(power)
        # Make sure that if power should be off then it is
        if state == "off":
            turn_off()
        # Long duration pulse width modulation
        for x in range(1, 100):
            if power > x:
                if state == "off":
                    state = "on"
                    print("On")
                    turn_on()
            else:
                if state == "on":
                    state = "off"
                    print("Off")
                    turn_off()
            sleep(1)


def loop():
    while True:
        sleep(1000)


if on_pi:
    b = sched.add_date_job(start_up, datetime.now() + timedelta(seconds=2))
else:
    b = sched.add_date_job(loop, datetime.now() + timedelta(seconds=2))


def event_stream():
    temp = tempdata()
    print(temp)
    yield 'event: temp\n' + 'data: ' + str(temp) + '|' + str(target/1000) + '\n\n'


try:
    @app.route('/my_event_source')
    def sse_request():
        return Response(event_stream(), mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        return render_template("test.html")

    @app.route('/1', methods=['POST'])
    def set_target():
        global target
        a = request.form.get('a', 'something is wrong', type=int)

        target = int(a * 1000)
        return jsonify({'1': ''})

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=89)
finally:
    print('done')