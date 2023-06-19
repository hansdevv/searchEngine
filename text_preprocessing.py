import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, norm=None, smooth_idf=True)

def preprocess_documents(documents):
	Stemmer = StemmerFactory()
	StopWord = StopWordRemoverFactory().create_stop_word_remover()
	stemmer = Stemmer.create_stemmer()
	docs = []

	for item in documents:
		doc = item[:-1]
		words_to_remove = ["ADVERTISEMENT", "SCROLL TO RESUME CONTENT"]
		for word in words_to_remove:
			doc = doc.replace(word, "")
		doc = doc.lower()
		doc = re.sub(r"\d+", "", doc)
		doc = re.sub(r"[%s]" % re.escape(string.punctuation), ' ', doc)
		doc = doc.strip()
		doc = StopWord.remove(doc)
		doc = stemmer.stem(doc)
		docs.append(doc)

	return docs

def calculate_tfidf(documents):
	count_vectorizer = CountVectorizer()
	word_count_vectorizer = count_vectorizer.fit_transform(documents)
	df = pd.DataFrame(word_count_vectorizer.T.toarray(), index=count_vectorizer.get_feature_names_out())
	tfidf_transform = TfidfTransformer()
	x = tfidf_transform.fit_transform(word_count_vectorizer)
	idf = pd.DataFrame({'feature_names': count_vectorizer.get_feature_names_out(), 'idf_weights': tfidf_transform.idf_})
	x = vectorizer.fit_transform(documents)
	tfidf = pd.DataFrame(x.T.toarray(), index=vectorizer.get_feature_names_out())
	
	return tfidf



def calculate_cosine_similarity(query, documents):
	tfidf_matrix = vectorizer.fit_transform(documents + [query])
	cosine_similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])

	if cosine_similarities is not None:
		similarity_scores = cosine_similarities.flatten()
	else:
		similarity_scores = []

	return similarity_scores