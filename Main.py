import json
from CyberPuerta import CyberpuertaScraper

def load_config():
	with open('config.json', 'r') as file:
		return json.load(file)

if __name__ == "__main__":
	config = load_config()
	for site_config in config['sites']:
		scraper = CyberpuertaScraper(site_config)  # Asume que todas las páginas pueden ser scrapeadas con la misma clase
		scraper.navigate_to(site_config['url'])
		scraper.extract_product_data()
		scraper.save_to_excel(site_config['file_name'])
		scraper.quit()