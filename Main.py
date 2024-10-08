import json
from CyberPuerta import CyberpuertaScraper
from LnbpScraper import LNBPScraperClass
from TiobeScraper import ProgrammingLanguagesScraper
from PowerBallScrapper import PowerBallScraperClass

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)
    
def get_scraper(site_config):
    if site_config['name'] == 'CyberPuerta':
        return CyberpuertaScraper(site_config)
    elif site_config['name'] == 'LNBP':
        return LNBPScraperClass(site_config)
    elif site_config['name'] == 'TIOBE':
        return ProgrammingLanguagesScraper(site_config)
    elif site_config['name'] == 'PowerBall':
        return PowerBallScraperClass(site_config)
    else:
        raise ValueError("Tipo de scraper no soportado")

if __name__ == "__main__":
    config = load_config()
    for site_config in config['sites']:
        scraper = get_scraper(site_config)
        scraper.navigate_to(site_config['url'])
        scraper.extract_product_data()
        scraper.quit()