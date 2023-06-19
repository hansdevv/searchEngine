import pandas as pd
from flask import Flask, render_template, request
from web_scrap import scrape_and_save_articles
from text_preprocessing import preprocess_documents, calculate_tfidf, calculate_cosine_similarity

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/search', methods=['GET'])
def scrape_and_process():
	url = "https://www.detik.com/search/searchall?query="
	query = request.args.get('query')
	pages = 2
	output_file = "articles.csv"

	# scrap dan simpan articles
	scrape_and_save_articles(url, query, pages, output_file)

	# baca dok hasil scrap
	data = pd.read_csv(output_file)

	# Preprocess the documents
	preprocessed_docs = preprocess_documents(data['content'].tolist())
	pd.DataFrame(preprocessed_docs).to_csv('prepocessed_document.csv', index=False, encoding='utf-8')

	# hitung TF-IDF
	tfidf = calculate_tfidf(preprocessed_docs)
	pd.DataFrame(tfidf).to_csv('tf_idf.csv', index=False, encoding='utf-8')

	# hitung cosine similarity dengan the query
	similarity_scores = calculate_cosine_similarity(query, preprocessed_docs)
	pd.DataFrame(tfidf).to_csv('similarity_scores.csv', index=False, encoding='utf-8')

	# tambah cosine similarity scores ke data DataFrame
	data['cosineSimilarity'] = similarity_scores.flatten()

	# urutkan data untuk ditampilkan berdasar nilai cos sim yang paling besar dulu
	data = data.sort_values(by='cosineSimilarity', ascending=False)

	return render_template('results.html', data=data, query = query)


if __name__ == '__main__':
	app.run(debug=True)
