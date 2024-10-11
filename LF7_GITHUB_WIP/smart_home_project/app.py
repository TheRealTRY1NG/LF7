from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import json
import schedule
import time
import threading
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from mock_gpio import GPIO

app = Flask(__name__)
app.secret_key = 'supersecretkey'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

routines = []
try:
    with open('routines.json', 'r') as f:
        routines = json.load(f)
except FileNotFoundError:
    with open('routines.json', 'w') as f:
        json.dump([], f)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html', routines=routines)

@app.route('/add_routine', methods=['POST'])
@login_required
def add_routine_route():
    routine = {
        'name': request.form['name'],
        'time': request.form['time'],
        'action': request.form['action']
    }
    routines.append(routine)
    with open('routines.json', 'w') as f:
        json.dump(routines, f)
    schedule.every().day.at(routine['time']).do(lambda action=routine['action']: turn_on_led(action))
    return redirect(url_for('index'))

@app.route('/delete_routine/<int:index>')
@login_required
def delete_routine(index):
    routine = routines.pop(index)
    with open('routines.json', 'w') as f:
        json.dump(routines, f)
    schedule.clear(routine['time'])
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

def turn_on_led(action):
    print(f"Turning on {action}")
    GPIO.output(LED_PIN, GPIO.HIGH)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=run_scheduler).start()
    app.run(host='0.0.0.0', port=5000)