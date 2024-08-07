from ScraperBase import ScraperBaseClass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class ProgrammingLanguagesScraper(ScraperBaseClass):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.language_names = []
        self.rank_2024 = []
        self.rank_2023 = []
        self.change = []
        self.ratings = []
        self.change_in_ratings = []

    def extract_product_data(self):
        try:
            self.driver.get(self.config['url'])
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.config['actions'][0]['selector_name']))
            )
            rows = table.find_elements(
                By.CSS_SELECTOR, self.config['actions'][1]['selector_name'])

            for row in rows:
                self.rank_2024.append(row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][2]['selector_name']).text)
                self.rank_2023.append(row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][3]['selector_name']).text)

                try:
                    change_element = row.find_element(
                        By.CSS_SELECTOR, self.config['actions'][4]['selector_name'])
                    self.change.append(change_element.get_attribute(
                        'src') if change_element.tag_name == 'img' else change_element.text)
                except:
                    self.change.append('N/A')

                self.language_names.append(row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][5]['selector_name']).text)
                self.ratings.append(row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][6]['selector_name']).text)
                self.change_in_ratings.append(row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][7]['selector_name']).text)

            print(
                f"Datos de lenguajes de programación extraídos: {len(self.language_names)}")

        except Exception as e:
            print(f"Error durante la extracción de datos: {e}")

    def save_to_excel(self, filename):
        try:
            min_length = min(len(self.rank_2024), len(self.rank_2023), len(self.change), len(self.language_names), len(self.ratings), len(self.change_in_ratings))
            df = pd.DataFrame({
                'Rank 2024': self.rank_2024[:min_length],
                'Rank 2023': self.rank_2023[:min_length],
                'Change': self.change[:min_length],
                'Programming Language': self.language_names[:min_length],
                'Ratings': self.ratings[:min_length],
                'Change in Ratings': self.change_in_ratings[:min_length]
            })
            df.to_excel(filename, index=False)
            print(f"Datos guardados exitosamente en {filename}")
        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")