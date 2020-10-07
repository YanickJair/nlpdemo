# NLP Demo

This is a Demo project working on Natural Processing Language testing some fundamentals use cases of NLP such as:
  * Sentiment Analysis: Try to predict if a text (i.e. review, comment) is positive or negative
  * Question Answer: Given a large text, try to extract answers by asking questions on top of the text.
  * Summarization: Summarize a text without losing the context.
  * Word Analogy: Find the nearest neighbor word based in a corpus input
  * Text Mining: This consists of extracting information from a text, such as verbs, person's name, entities, countries, places, etc.
  * And some more
  
# Most important dependecies:
1. [Spacy IO](https://spacy.io/) - Industrial-Strength Natural Language Processing
2. [Hugging Face](https://huggingface.co/) - State-of-the-art Natural Language Processing for PyTorch and TensorFlow 2.0
3. [Pytorch](https://pytorch.org/) - An open source machine learning framework that accelerates the path from research prototyping to production deployment.

# The project is divided into two parts
1. NLP API - A Flask based api.
2. NLP Web APP - Vue Js application


# Python API
 * ```yelp_dataset(start=0, end=10)``` - return a range of reviews with starting and end postion. The reviews are located in dataset/yelp.csv file
 * ```analyze(request)``` - Perform text mining on a POST request containing a text as input. The text mining are based on a configuration input array containing the desired mining actions: verbs, person, country etc
 * ```sentiment_analysis(request)``` - Perform a sentiment analysis on a given text input and return a dictionary ```{LABEL, score}```. LABEL can be eighter *POSITIVE* or *NEGATIVE*. The *score* is the acurracy probability
 * ```answer_question(request)``` - inputs {text, question}. Extract answer from the input text based on the input question. Returns a answer dictionary ```{answer}```
 * ```summarizer(request)``` - inputs {text}. Summarize the input text. max_length for the summarization is ```round(int(len(data["text"]) * 0.2) / 2)``` and min_length is ```30```. 

# Examples

1. A question answering solution
 ![photo_2020-09-28_13-13-25](https://user-images.githubusercontent.com/26607519/94431492-44ba2b00-018d-11eb-82f3-ad72a3348527.jpg)

2. Text Summarization
 ![photo_2020-09-28_13-13-32](https://user-images.githubusercontent.com/26607519/94431755-9a8ed300-018d-11eb-8efe-a263b0d913d6.jpg)


# Note
The repository is still under work. This is just an intro README to give the big picture of the project.
