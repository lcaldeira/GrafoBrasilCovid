#pip install selenium
#pip3 install webdriver-manager

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def wait_for_downloads(folder):
    print("Waiting for downloads.", end="")
    time.sleep(1)
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(folder)]):
        print(".", end="")
        time.sleep(1)
    print("done!")


# pré-configurações
serv = Service(ChromeDriverManager().install())

target_path = os.path.abspath(os.getcwd()) + '/dados/fonte/IBGE_LogTransp'
_ = os.system('mkdir -p ' + target_path)

confs = webdriver.ChromeOptions()
confs.add_experimental_option("prefs", {
	"download.default_directory" : target_path
})

driver = webdriver.Chrome(service=serv, options=confs)
driver.implicitly_wait(15)

# abre a página do IBGE de logística de transporte e efetua o download
driver.get("https://www.ibge.gov.br/geociencias/cartas-e-mapas/redes-geograficas/15793-logistica-dos-transportes.html?=&t=downloads")
driver.find_element(by=By.XPATH, value="//a[text()='base_de_dados']").click()
driver.find_element(by=By.XPATH, value="//a[text()='2014.zip']").click()

# espera o dowload acabar e encerra
wait_for_downloads(target_path)
driver.quit()
