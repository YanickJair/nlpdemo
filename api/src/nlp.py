from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

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

def get_persons(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == 'PERSON']

def get_countries(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == 'GPE']

def get_entities(doc):
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "ORG"]

def get_animals(doc):
    try:
        nlp.add_pipe(animal_component)
    except ValueError as ve:
        return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "ANIMAL"]

def sentiment_analysis(text):
    assert isinstance(text, str)
    from transformers import pipeline
    classifier = pipeline("sentiment-analysis")
    return classifier(text)

def get_verbs(doc):
    return [(token.text, token.pos_) for token in doc if token.pos_ == "VERB" or token.pos_ == "AUX"]