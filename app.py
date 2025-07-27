from flask import Flask
import socket
import requests

app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()
    try:
        ip_address = requests.get("https://api.ipify.org").text
    except Exception:
        ip_address = "Could not fetch IP"
    
    return f"""
    <h1>Hello from Anisble -> Flask deployment App!</h1>
    <p><strong>Hostname:</strong> {hostname}</p>
    <p><strong>Public IP:</strong> {ip_address}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

