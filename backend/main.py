from flask import Flask, send_file
import os
import socket

def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # Use a non-routable IP for UDP
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(SCRIPT_DIR)
WWW_DIR = os.path.join(SCRIPT_DIR, "www")
print(WWW_DIR)

app = Flask(__name__)

# API Routes:
## Main Website:
@app.route("/")
def index():
    return send_file("./www/index.html"), 200

## Grabing Website Files (like style.css)
@app.route("/www/<filename>")
def www_access(filename):
    filepath = os.path.join(WWW_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath), 200
    else:
        return f"<h1>404</h1><p>Could not find the file {filename}</p>", 404
    
## Find Device:
@app.route("/source")
def source():
    device_data = {
        'app_confirm': 'localshare',
        'local_ip': get_primary_ip(),
        'name': 'test',
    }


app.run(host="0.0.0.0", port=8080, debug=True)