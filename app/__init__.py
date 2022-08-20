from flask import Flask
import sys
import signal

def handler(sig, frame):
    print(f'YOU CALLED ME WITH {sig}')
    from app.routes import session
    print("Close MYSQL session")
    session.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

app = Flask(__name__)

from app import routes