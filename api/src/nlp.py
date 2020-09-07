import spacy
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

def make_doc(TEXT):
    return nlp(TEXT)    

def animal_component(doc):
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
    matcher = PhraseMatcher(nlp.vocab)
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