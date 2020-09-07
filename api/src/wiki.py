import wikipedia

def get_result(word=None, sentences=2):
    res = None
    try:
        if word is not None:
            res = wikipedia.summary(word, sentences=sentences)
    except:
        raise
    return res