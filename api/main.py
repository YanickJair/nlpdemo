from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from src import wiki
from src import nlp

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
        res = []
        if "persons" in data["configs"]:
            res.append({
                "PERSONS": nlp.get_persons(doc)
            })
        if "entities" in data["configs"]:
            res.append({
                "ENTITIES": nlp.get_entities(doc)
            })

        if "countries" in data["configs"]:
            res.append({
                "COUNTRIES": nlp.get_countries(doc)
            })
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
