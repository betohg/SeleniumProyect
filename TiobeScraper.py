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
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.config['selectors']['table']['top20_table']))
            )
            rows = table.find_elements(
                By.CSS_SELECTOR, self.config['selectors']['row']['top20_row'])

            for row in rows:
                self.rank_2024.append(row.find_element(
                    By.CSS_SELECTOR, self.config['selectors']['text']['rank_current']).text)
                self.rank_2023.append(row.find_element(
                    By.CSS_SELECTOR, self.config['selectors']['text']['rank_previous']).text)

                # change_element = row.find_element(
                #     By.CSS_SELECTOR, self.config['selectors']['text']['change'])
                # self.change.append(change_element.get_attribute(
                #     'alt') if change_element.tag_name == 'img' else change_element.text)

                self.language_names.append(row.find_element(
                    By.CSS_SELECTOR, self.config['selectors']['text']['language_name']).text)
                self.ratings.append(row.find_element(
                    By.CSS_SELECTOR, self.config['selectors']['text']['rating']).text)
                self.change_in_ratings.append(row.find_element(
                    By.CSS_SELECTOR, self.config['selectors']['text']['change_percentage']).text)

            print(
                f"Datos de lenguajes de programación extraídos: {len(self.language_names)}")

        except Exception as e:
            print(f"Error durante la extracción de datos: {e}")

    def save_to_excel(self, filename):
        try:
            df = pd.DataFrame({
                'Rank 2024': self.rank_2024,
                'Rank 2023': self.rank_2023,
                # 'Change': self.change,
                'Programming Language': self.language_names,
                'Ratings': self.ratings,
                'Change in Ratings': self.change_in_ratings
            })
            df.to_excel(filename, index=False)
            print(f"Datos guardados exitosamente en {filename}")
        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")
