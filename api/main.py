from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from src import wiki
from src import nlp
from src import get_dataset

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def home():
    data = {
        "search": wiki.get_result("Like")
    }
    print(data)
    return jsonify(data)

@app.route("/analysis", methods=["POST"])
@cross_origin()
def analysis():
    if request.method == 'POST':
        data = request.get_json()
        doc = nlp.make_doc(data["text"])
        res = {}
        if "persons" in data["configs"]:
            res["PERSONS"] = nlp.get_persons(doc)
        if "entities" in data["configs"]:
            res["ENTITIES"] = nlp.get_entities(doc)  

        if "countries" in data["configs"]:
            res["COUNTRIES"] = nlp.get_countries(doc)
    return jsonify(res)

@app.route("/dataset/<int:size>", methods=["GET"])
@cross_origin()
def dataset(size=10):
    print(size)
    if request.method == 'GET':
        dataset = get_dataset.load()
        return jsonify(dataset[0:size:])

@app.route("/sentiment-analysis", methods=["POST"])
@cross_origin()
def sentiment_analysis():
    assert request.method == "POST"
    data = request.get_json()
    res = nlp.sentiment_analysis(data["text"])
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
