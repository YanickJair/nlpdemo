from flask import Flask
app = Flask(__name__)
import api.views

if __name__ == "api":
    app.run(host="0.0.0.0", port=5000)