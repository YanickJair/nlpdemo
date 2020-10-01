import time

import numpy as np

from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

from annoy import AnnoyIndex

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
def sentiment_analysis(text, classifier):
    assert isinstance(text, str)
    from transformers import pipeline
    return classifier(text)

@timer
def get_verbs(doc):
    return [
        (token.text, token.pos_) for token in doc if token.pos_ == "VERB" or token.pos_ == "AUX"
    ]

""" 
Extract question's response from a large text
"""
def answer_question(question=None, TEXT=None, tokenizer=None, model=None):
    answer = None
    try:
        import torch

        inputs = tokenizer(
            question,
            TEXT,
            add_special_tokens=True,
            return_tensors='pt'
        )
        input_ids = inputs["input_ids"].tolist()[0]

        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = model(**inputs)

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        #* Compute the possible answer to the question
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(
            input_ids[answer_start:answer_end]
        ))
    except:
        raise
    return answer

""" 
Word Analogy Class
"""
class WorldAnalogyModel(object):
    def __init__(self, word_to_index, word_vectors):
        """ 
        Args:
            word_to_index (dict)
            word_vectors (nupmy.array)
        """
        self.word_to_index = word_to_index
        self.word_vectors = word_vectors

        self.index_to_word = { v: k for k, v in self.word_to_index.items() }
        self.index = AnnoyIndex(len(word_vectors[0]), metric='euclidean')

        for _, i in self.word_to_index.items():
            self.index.add_item(i, self.word_vectors[i])
        self.index.build(50)

    @classmethod
    def from_embeddings_file(cls, embedding_file):
        assert embedding_file
        """ 
        Args:
            embedding_file (str) -> path to the csv file
        """
        word_to_index = {}
        word_vectors = []
        with open(embedding_file) as fp:
            for line in fp.readlines():
                line = line.split(" ")
                word = line[0]
                vec = np.array([ float(x) for x in line[1:] ])
                
                word_to_index[word] = len(word_to_index)
                word_vectors.append(vec)
        return cls(word_to_index, word_vectors)

    def get_embedding(self, word):
        """
        Args:
            word (str)
        Returns:
            numpy.array
        """
        return self.word_vectors[self.word_to_index[word]]

    def get_closest_to_vector(self, vector, n=1):
        """Given a vector, return its n nearest neighbors
        Args:
            vector (np.array)
            n (int) -> the number of neighbors to return
        Returns:
            [str,str...] -> words nearest to the given vector
        """
        nn_indices = self.index.get_nns_by_vector(vector, n)
        return [self.index_to_word[neighbor] for neighbor in nn_indices]
    
    def compute_analogy(self, word1, word2=None, word3=None):
        """
        Args:
            word1 (str)
            word2 (str)
            word3 (str)
        Returns:
            closest_words (list) -> a list of nearest neighbors
        """
        vec = self.get_embedding(word1)
        n = 8

        if word2 and word3:
            n = 4
            vec2 = self.get_embedding(word2)
            vec3 = self.get_embedding(word3)
            
            # Symple hypothesis: Analogy is a spatial relationship
            spatial_relationship = vec2 - vec
            vec = vec3 + spatial_relationship
        
        closest_words = self.get_closest_to_vector(vec, n=n)
        existng_words = set([word1, word2, word3])
        closest_words = [word for word in closest_words if word not in existng_words]
        
        return closest_words