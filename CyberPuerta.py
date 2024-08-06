from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from ScraperBase import ScraperBaseClass

class CyberpuertaScraper(ScraperBaseClass):
	def __init__(self, config):
		super().__init__(config)
		self.config = config
		self.product_names = []
		self.product_prices = []
		self.product_availabilities = []

	def extract_product_data(self):
		try:
			for action in self.config['actions']:
				if action['action'] == 'click':
					element = WebDriverWait(self.driver, 10).until(
						EC.element_to_be_clickable(
							(getattr(By, action['selector']), action['selector_name'])
						)
					)
					element.click()
				elif action['action'] == 'find':
					element = WebDriverWait(self.driver, 20).until(
						EC.presence_of_element_located(
							(getattr(By, action['selector']), action['selector_name'])
						)
					)
				elif action['action'] == 'find_multiple':
					elements = element.find_elements(
						getattr(By, action['selector']), action['selector_name']
					)
					for item in elements:
						product_name = item.find_element(
							By.CSS_SELECTOR, self.config['actions'][3]['selector_name']).text
						product_price = item.find_element(
							By.CSS_SELECTOR, self.config['actions'][4]['selector_name']).text
						product_availability = item.find_element(
							By.CSS_SELECTOR, self.config['actions'][5]['selector_name']).text

						self.product_names.append(product_name)
						self.product_prices.append(product_price)
						self.product_availabilities.append(product_availability)

			print(f"Productos extraídos: {len(self.product_names)}")

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