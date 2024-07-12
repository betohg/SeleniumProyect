from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import pandas as pd

edge_options = Options()
edge_options.add_argument('--ignore-certificate-errors')
edge_options.add_argument('--allow-insecure-localhost')
edge_options.add_argument('--allow-running-insecure-content')

driver = webdriver.Edge(options=edge_options)

try:
    driver.get("https://www.cyberpuerta.mx/")

    categoria_promociones = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/Promociones/']"))
    )
    categoria_promociones.click()

    product_names = []
    product_prices = []
    product_availabilities = []

    def extract_product_data():
        product_list = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "productList"))
        )
        product_items = product_list.find_elements(By.CSS_SELECTOR, "li.cell.productData")

        for item in product_items:
            product_name = item.find_element(By.CSS_SELECTOR, "a.emproduct_right_title").text
            product_price = item.find_element(By.CSS_SELECTOR, "div.emproduct_right_price_left > label.price").text
            product_availability = item.find_element(By.CSS_SELECTOR, "div.emstock > span").text

            product_names.append(product_name)
            product_prices.append(product_price)
            product_availabilities.append(product_availability)

    extract_product_data()

    i = 0
    while i < 2:
        try:
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next"))
            )
            next_page_button.click()

            extract_product_data()
            i += 1

        except:
            break

    df = pd.DataFrame({
        'Nombre del Producto': product_names,
        'Precio': product_prices,
        'Disponibilidad': product_availabilities
    })

    df.to_excel('productos_cyberpuerta.xlsx', index=False)
    print("Datos guardados exitosamente en productos_cyberpuerta.xlsx")

finally:
    driver.quit()
