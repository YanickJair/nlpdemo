from flask import Flask
app = Flask(__name__)
import api.views

if __name__ == "api":
    app.run(host="10.114.0.2", port=5000)