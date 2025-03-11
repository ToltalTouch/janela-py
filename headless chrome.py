from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from pywinauto.application import Application
import os
import logging
import time

# O caminho do arquivo que você quer enviar
atual_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(atual_dir, "manual-pdf", "arquivo.pdf")
chromedriver_path = os.path.join(atual_dir, "chromedriver-win64", "chromedriver.exe")

chrome_options = Options()
chrome_options.add_argument("--maximized")
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(atual_dir, "log.txt")),
        logging.StreamHandler()
    ]
)
logging.info(f'Caminho arquivo {caminho_arquivo}')

# Ele vai para a página da internet
driver.get("https://www.ilovepdf.com/pt/pdf_para_jpg")

# Ele espera o botão estar presente e clica nele
botao_upload = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="pickfiles"]'))
)
botao_upload.click()

# Ele espera a janelinha do Windows aparecer
time.sleep(2)

# Ele digita o caminho do arquivo
app = Application().connect(title_re="Abrir")
dlg = app.window(title_re="Abrir")
dlg['Edit'].set_edit_text(caminho_arquivo)
dlg.AbrirButton.click()

# Ele espera um pouco para você ver o que aconteceu
time.sleep(5)

# Ele fecha o navegador
driver.quit()