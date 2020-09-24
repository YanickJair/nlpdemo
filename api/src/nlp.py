import time

from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

time_spent = {}
labels = []
data = []

timed_phrase = set()

def get_timer():
    global time_spent
    return time_spent

def timer(func):
    def f(*args, **kwargs):
        global time_spent, labels, data, timed_phrase

        if func.__name__ == 'sentiment_analysis':
            key =  args[0] + ':' + func.__name__
            print(args)
        else:
            key =  args[0].text + ':' + func.__name__
        if key not in timed_phrase:
            before = time.perf_counter()
            rv = func(*args, **kwargs)
            after = time.perf_counter()

            labels.append(func.__name__)
            data.append(after - before)
            time_spent["labels"] = labels
            time_spent["data"] = data

            timed_phrase.add(key)
            return rv
    return f

def animal_component(doc, vocab):
    animals = [
        "Golden Retriever",
        "cat",
        "turtle",
        "dog",
        "fish",
        "Rattus norvegicus",
        "snake",
        "lion",
        "tigger"
    ]
    matcher = PhraseMatcher(vocab)
    mathes = matcher(doc)
    span = [Span(doc, start, end, label="ANIMAL") for matcher_id, start, end in mathes]
    doc.ents = span
    return doc

@timer
def get_persons(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == 'PERSON']

@timer
def get_countries(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == 'GPE']

@timer
def get_entities(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "ORG"]

@timer
def get_animals(doc):
    try:
        nlp.add_pipe(animal_component)
    except ValueError as ve:
        return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "ANIMAL"]

@timer
def sentiment_analysis(text):
    assert isinstance(text, str)
    from transformers import pipeline
    classifier = pipeline("sentiment-analysis")
    return classifier(text)

@timer
def get_verbs(doc):
    return [(token.text, token.pos_) for token in doc if token.pos_ == "VERB" or token.pos_ == "AUX"]