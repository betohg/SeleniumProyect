import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from ScraperBase import ScraperBaseClass

class PowerBallScraperClass(ScraperBaseClass):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.dates = []

    def extract_product_data(self):
        try:
            self.driver.get(self.config['url'])
            archive_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.config['actions'][0]['selector_name']))
            )
            result_containers = archive_container.find_elements(
                By.CSS_SELECTOR, self.config['actions'][1]['selector_name'])

            if not result_containers:
                print("No se encontraron contenedores de resultados.")
                return

            months_found = set()
            for result_container in result_containers:
                date_text = result_container.find_element(By.CSS_SELECTOR, self.config['actions'][2]['selector_name']).text.strip()
                month = date_text.split()[1]
                if month not in months_found:
                    self.dates.append(date_text)
                    months_found.add(month)
                if len(self.dates) == 3:
                    break

            print(f"Fechas de PowerBall extraídas: {self.dates}")

            # Hacer clic en el botón "Prize Breakdown" del primer resultado
            first_prize_breakdown_button = result_containers[0].find_element(By.CSS_SELECTOR, self.config['actions'][3]['selector_name'])
            first_prize_breakdown_button.click()

            # Esperar a que la tabla de premios esté presente
            prize_table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config['actions'][4]['selector_name']))
            )

            # Extraer datos de la tabla
            rows = prize_table.find_elements(By.TAG_NAME, 'tr')
            table_data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                cols = [col.text for col in cols]
                table_data.append(cols)

            # Guardar datos en el primer archivo Excel
            self.save_to_excel(self.dates[0], table_data)

        except IndexError as e:
            print(f"Error durante la extracción de datos: {e}")
        except Exception as e:
            print(f"Error durante la extracción de datos: {e}")

    def save_to_excel(self, date, table_data):
        try:
            clean_date = re.sub(r'[^\w\s-]', '', date).replace(' ', '_').replace('\n', '')
            filename = clean_date + '.xlsx'
            df = pd.DataFrame(table_data)
            df.to_excel(filename, index=False)
            print(f"Archivo Excel creado exitosamente: {filename}")

        except Exception as e:
            print(f"Error al guardar los archivos Excel: {e}")