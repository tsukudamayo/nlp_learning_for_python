from tfidf import TfidfModel

from summarize import summarize
from lib.db import load_docs_for_training, load_reviews_and_split_to_sentences


docs = load_docs_for_training()
tfidf = TfidfModel()
model, dictionary = tfidf.generate(docs)

target_id = 0

sentences_unfiltered = load_reviews_and_split_to_sentences(target_id)

summary_sentences = summarize(
    sentences_unfiltered, model, dictionary, max_characters=70, user_mmr=True, sent_limit=50
)
for sentence in summary_sentences:
    print(sentence.strip())


