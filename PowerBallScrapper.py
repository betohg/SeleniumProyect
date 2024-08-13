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

            for index, result_container in enumerate(result_containers[:len(self.dates)]):
                try:
                    # Obtener el href del botón "Prize Breakdown"
                    prize_breakdown_href = result_container.find_element(By.CSS_SELECTOR, self.config['actions'][3]['selector_name']).get_attribute("href")

                    # Si el href no es una URL completa, prepender el dominio principal
                    if not prize_breakdown_href.startswith("http"):
                        prize_breakdown_href = self.config['url'].split('/numbers')[0] + prize_breakdown_href

                    # Navegar a la página del "Prize Breakdown"
                    self.driver.get(prize_breakdown_href)

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

                    # Guardar datos en un archivo Excel para cada fecha
                    self.save_to_excel(self.dates[index], table_data)

                    # Regresar a la página principal de fechas
                    self.driver.back()

                    # Esperar a que la página vuelva a cargar los resultados
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, self.config['actions'][0]['selector_name']))
                    )

                except Exception as e:
                    print(f"Error durante la extracción de datos en la iteración {index + 1}: {e}")
                    continue  # Intentar con la siguiente fecha

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
