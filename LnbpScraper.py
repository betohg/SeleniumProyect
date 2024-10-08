from ScraperBase import ScraperBaseClass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class LNBPScraperClass(ScraperBaseClass):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.team_names = []
        self.team_stats = []

    def extract_product_data(self):
        try:
            self.driver.get(self.config['url'])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.config['actions'][0]['selector_name']))
            )
            print("Tabla de estadísticas de equipos encontrada.")

            teams_rows = self.driver.find_elements(
                By.CSS_SELECTOR, self.config['actions'][1]['selector_name'])

            if not teams_rows:
                print("No se encontraron filas de equipos.")
                return

            for team_row in teams_rows:
                team_name = team_row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][2]['selector_name']).text
                games_played = team_row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][3]['selector_name']).text
                games_won = team_row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][4]['selector_name']).text
                games_lost = team_row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][5]['selector_name']).text
                points = team_row.find_element(
                    By.CSS_SELECTOR, self.config['actions'][6]['selector_name']).text

                self.team_names.append(team_name)
                self.team_stats.append({
                    'Jugados': games_played,
                    'Ganados': games_won,
                    'Perdidos': games_lost,
                    'Puntos': points
                })

            print(f"Equipos extraídos: {len(self.team_names)}")

        except Exception as e:
            print(f"Error durante la extracción de datos: {e}")
            print(f"Total de equipos extraídos: {len(self.team_names)}")

    def save_to_excel(self, filename):
        df = pd.DataFrame(self.team_stats)
        df.insert(0, 'Nombre del Equipo', self.team_names)
        df.to_excel(filename, index=False)
        print(f"Datos guardados exitosamente en {filename}")