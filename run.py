#!venv/bin/python
from app import app
import os
from threading import Thread

def run_listen():
    os.system("python listen_time_task.py")
if __name__ == '__main__':
    t3 = Thread(target=run_listen)
    t3.start()
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)
