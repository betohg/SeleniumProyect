import json
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from abc import ABC, abstractmethod

class ScraperBaseClass(ABC):
	def __init__(self, config):
		self.config = config
		edge_options = Options()
		edge_options.add_argument('--ignore-certificate-errors')
		edge_options.add_argument('--allow-insecure-localhost')
		edge_options.add_argument('--allow-running-insecure-content')
		self.driver = webdriver.Edge(options=edge_options)

	@abstractmethod
	def extract_product_data(self):
		pass

	def navigate_to(self, url):
		self.driver.get(url)

	def quit(self):
		self.driver.quit()