from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import src
from src import get_dataset
from src import nlp as NLP

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

nlp = None
classifier = None
summarizer = None

@app.route("/")
@cross_origin()
def home():
    data = {
        "search": src.wiki.get_result("Like")
    }
    return jsonify(data)

@app.route("/analysis", methods=["POST"])
@cross_origin()
def analysis():
    assert nlp
    assert classifier
    assert summarizer

    if request.method == 'POST':
        import string

        data = request.get_json()
        doc = make_doc(data["text"].replace("@", ""))

        res = {}
        if "persons" in data["configs"]:
            res["PERSONS"] = NLP.get_persons(doc)
        if "entities" in data["configs"]:
            res["ENTITIES"] = NLP.get_entities(doc)  
        if "countries" in data["configs"]:
            res["COUNTRIES"] = NLP.get_countries(doc)
        if "verbs" in data["configs"]:
            res["VERBS"] = NLP.get_verbs(doc)
        if "sentiment" in data["configs"]:
            data = request.get_json()
            text = data["text"].translate(str.maketrans('', '', string.punctuation))
            sa = NLP.sentiment_analysis(text)
            print("SA: ", sa)
            res["SENTIMENT_ANALYSIS"] = sa
        if "summarize" in data["configs"]:
            summarized = summarizer(
                data["text"],
                max_length=118,
                min_length=30,
                do_sample=False
            )
            res["summarized"] = summarized[0]["summary_text"] 
        
        timer = NLP.get_timer()
        res["time_spent"] = timer
        
    return jsonify(res)

@app.route("/dataset/<int:size>", methods=["GET"])
@cross_origin()
def dataset(size=10):
    if request.method == 'GET':
        dataset = get_dataset.load()
        return jsonify(dataset[0:size:])

@app.route("/yelp-dataset/<int:rating>", methods=["GET"])
@cross_origin()
def yelp_dataset(rating=5):
    try:
        if request.method == 'GET':
            dataset = get_dataset.load_yelp_reviews()
            return jsonify(dataset[rating])
    except:
        raise

@app.route("/sentiment-analysis", methods=["POST"])
@cross_origin()
def sentiment_analysis():
    assert request.method == "POST"

    import string 
    
    data = request.get_json()
    text = data["text"].translate(str.maketrans('', '', string.punctuation))
    res = NLP.sentiment_analysis(text)
    return jsonify(res)

def make_doc(TEXT):
    return nlp(TEXT)

with app.app_context():
    nlp
    classifier

    from transformers import pipeline
    
    import spacy
    from spacy.tokens import Span
    from spacy.matcher import PhraseMatcher

    from transformers import pipeline

    summarizer = pipeline("summarization")
    classifier = pipeline("sentiment-analysis")

    nlp = spacy.load("en_core_web_sm")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)