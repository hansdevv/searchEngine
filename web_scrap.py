import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool

def scrape_articles(article_url):
	data = []
	response = requests.get(article_url)
	soup = BeautifulSoup(response.text, "html.parser")
	articles = soup.select("article")
	content = ''

	for article in articles:
		title = article.select_one("h2.title").get_text()
		linkImg = article.select_one("img")["src"]
		shortDescription = article.select_one("p").get_text()
		articleLink = article.select_one("a")["href"]

		article_soup = BeautifulSoup(requests.get(articleLink).text, "html.parser")
		article_body = article_soup.select_one("div.detail__body-text.itp_bodycontent")
		content = article_body.text if article_body else "Lorem ipsum dolor sit amet consectetur adipisicing elit."

		data.append({
			"title": title,
			"linkImg": linkImg,
			"shortDescription": shortDescription,
			"articleLink": articleLink,
			"content": content
		})

	return data

def scrape_and_save_articles(url, query, pages, output_file):
	search_url = url + query

	# Using multiprocessing to perform parallel scraping
	with Pool() as pool:
		urls = [search_url + f"&page={page}" for page in range(1, pages + 1)]
		results = pool.map(scrape_articles, urls)

	data = [item for sublist in results for item in sublist]
	pd.DataFrame(data).to_csv(output_file, index=False, encoding='utf-8')
