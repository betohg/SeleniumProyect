from ScraperBase import ScraperBaseClass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class CyberpuertaScraper(ScraperBaseClass):
	def __init__(self, config):
		super().__init__(config)
		self.config = config
		self.product_names = []
		self.product_prices = []
		self.product_availabilities = []

	def extract_product_data(self):
		try:
			categoria_promociones = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located(
					(By.CSS_SELECTOR, self.config['categoria_promociones_selector']))
			)
			print("Categoría de promociones encontrada.")
			categoria_promociones.click()

			i = 0
			while i < 2:
				product_list = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located(
						(By.ID, self.config['product_list_selector']))
				)
				print("Lista de productos encontrada.")
				product_items = product_list.find_elements(
					By.CSS_SELECTOR, self.config['product_item_selector'])

				if not product_items:
					print("No se encontraron productos.")
					break

				for item in product_items:
					product_name = item.find_element(
						By.CSS_SELECTOR, self.config['product_name_selector']).text
					product_price = item.find_element(
						By.CSS_SELECTOR, self.config['product_price_selector']).text
					product_availability = item.find_element(
						By.CSS_SELECTOR, self.config['product_availability_selector']).text

					self.product_names.append(product_name)
					self.product_prices.append(product_price)
					self.product_availabilities.append(product_availability)

				print(f"Productos extraídos: {len(self.product_names)}")

				next_page_button = WebDriverWait(self.driver, 10).until(
					EC.element_to_be_clickable(
						(By.CSS_SELECTOR, self.config['next_page_selector']))
				)
				next_page_button.click()

				i += 1

		except Exception as e:
			print(f"Error durante la extracción de datos: {e}")
			print(f"Total de nombres de productos extraídos: {len(self.product_names)}")

	def save_to_excel(self, filename):
		df = pd.DataFrame({
			'Nombre del Producto': self.product_names,
			'Precio': self.product_prices,
			'Disponibilidad': self.product_availabilities
		})
		df.to_excel(filename, index=False)
		print(f"Datos guardados exitosamente en {filename}")