from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.ktronix.com/celulares/telefonos-celulares/iphone/c/BI_M009_KTRON?q=%3Arelevance%3Afamilias-celulares%3AIphone+13%3Afamilias-celulares%3AIphone+13+Pro%3Afamilias-celulares%3AIphone+13+Pro+max%3Afamilias-celulares%3AIphone+13+mini%3Afamilias-celulares%3AiPhone+SE%3Afamilias-celulares%3AiPhone+11%3Afamilias-celulares%3AiPhone+XR%3Afamilias-celulares%3AiPhone+11+Pro%3Afamilias-celulares%3AiPhone+12%3Afamilias-celulares%3AiPhone+12+mini'
driver.get(url)
scriptArray = """return localStorage.products;"""
result = driver.execute_script(scriptArray)

list = eval(result)

print("Productos extraídos de ktronix:", len(list))
print(list)


def imprimirDatos(data):
    for item in data:
        print(item)


def addProduct(product):
    response = requests.post(
        'https://gf45e9f189895df-data1warehouse.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/data/v1/productos_competencia',
        data={
            "name": product["name"],
            "color": product["variant"].split(":")[1],
            "price": product["price"],
            "brand": product["brand"],
            "brand_category": product["list"],
            "registration_date": "25/03/2022",
        })


print("Cargando productos al Data webhouse...")

for product in list:
    addProduct(product)

response = requests.get(
    "https://gf45e9f189895df-data1warehouse.adb.us-ashburn-1.oraclecloudapps.com/ords/admin/data/v1/productos_competencia")
returnItems = json.loads(response.text)["items"]

if len(returnItems) == 0:
    print("No hay productos")
else:
    print("Datos del Data webhouse:")
    imprimirDatos(returnItems)
