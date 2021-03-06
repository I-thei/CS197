import time

import pandas as pd
import spacy


def process_tweets(filename):
    df = pd.read_csv(filename, delimiter=',')
    nlp = spacy.load('en')
    new_words = ["don't", "dont"]

    for word in new_words:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True

    start = time.time()
    df['Parsed'] = df['text'].apply(nlp)

    lemmas = []

    for doc in df['Parsed']:
        temp = []
        for w in doc:
            if not w.is_stop and not w.is_punct and not w.like_num and len(
                    w.lemma_) > 2 and '@' not in w.lemma_ and 'http' not in w.lemma_:
                temp.append(str.lower(w.lemma_))
        lemmas.append(temp)
    df['lemmas'] = lemmas

    df.to_csv(filename)
