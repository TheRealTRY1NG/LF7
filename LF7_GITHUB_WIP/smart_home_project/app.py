from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from scheduler import *
import os
import json
import schedule
import scheduler
import time
import threading

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

#To-Do @LUCAS
@app.route('/add_routine', methods=['POST'])
@login_required
def add_routine_route():  
    routine = {
        #Name of the routine (should be unique)
        'name': request.form['routineName'],
        #Time of the routines start
        'time': request.form['routineTime']
    }
    routines.append(routine)
    with open('routines.json', 'w') as f:
        json.dump(routines, f)

    #for each selected device add:
        routine_action = {
            #Name of the device (should be unique)
            'device': request.form['device'],
            #State the device should go into ("ON" or "OFF")
            'state': request.form['state'],
            #Offset for devices state change
            'offset': request.form['offset']
        }    
            
        with open(routine['name'] + '.json', 'w') as f:
            json.dump(routine_action, f)

        scheduler.add_Routine(routine, routine_action)
   
    return redirect(url_for('index'))

@app.route('/delete_routine/<int:index>')
@login_required
def delete_routine(index):
    routine = routines.pop(index)

    with open('routines.json', 'w') as f:
        json.dump(routines, f)

    os.remove(routine['name'] + '.json')

    scheduler.remove_Routine(routine)

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
  
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=run_scheduler).start()
    app.run(host='0.0.0.0', port=5000)