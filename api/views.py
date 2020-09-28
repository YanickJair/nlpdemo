from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import api.src as src
from api.src import get_dataset
from api.src import nlp as NLP

from api import app

# app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

nlp = None
classifier = None
summarizer = None
tokenizer = None
question_model = None

""" @app.route("/")
@cross_origin()
def home():
    data = {
        "search": src.wiki.get_result("Like")
    }
    return jsonify(data) """

@app.route('/')
def home():
   return "hello world!"

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
            res["SENTIMENT_ANALYSIS"] = sa
            
        timer = NLP.get_timer()
        res["time_spent"] = timer
    print(res)
    return jsonify(res)

@app.route("/dataset/<int:size>", methods=["GET"])
@cross_origin()
def dataset(size=10):
    if request.method == 'GET':
        dataset = get_dataset.load()
        return jsonify(dataset[0:size:])

@app.route("/yelp-dataset/<int:start>/<int:end>", methods=["GET"])
@cross_origin()
def yelp_dataset(start=0, end=10):
    try:
        if request.method == 'GET':
            dataset, pages = get_dataset.load_yelp_reviews(start=start, end=end)
            return jsonify({
                "dataset": dataset,
                "pages": pages
            })
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

@app.route("/answer-question", methods=["POST"])
@cross_origin()
def answer_question():
    assert request.method == "POST"

    data = request.get_json()
    answer = NLP.answer_question(
        question=data["question"],
        TEXT=data["text"],
        tokenizer=tokenizer,
        model=question_model
    )
    return jsonify({"answer": answer})        

@app.route("/summarizer", methods=["POST"])
@cross_origin()
def summarizer():
    assert request.method == "POST"

    data = request.get_json()
    summarized = summarizer(
        data["text"],
        max_length=50,
        min_length=30,
        do_sample=False
    )
    summary_text = summarized[0]["summary_text"]
    return jsonify({"summary_text": summary_text})  

def make_doc(TEXT):
    return nlp(TEXT)

with app.app_context():
    try:
        nlp
        classifier

        from transformers import pipeline
        
        import spacy
        from spacy.tokens import Span
        from spacy.matcher import PhraseMatcher
        
        from transformers import AutoTokenizer, AutoModelForQuestionAnswering
        import torch

        from transformers import pipeline

        #* Summarization model
        summarizer = pipeline("summarization")

        #* Sentiment Analysis model
        classifier = pipeline("sentiment-analysis")

        #* Instantiate a tokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        #* Question Answer mdoel
        question_model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

        nlp = spacy.load("en_core_web_sm")
    except:
        raise
