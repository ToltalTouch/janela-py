import os
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Inicializa o driver do Chrome fora da função para evitar problemas de escopo
dir_atual = os.path.dirname(os.path.abspath(__file__))

chromedriver_path = os.path.join(dir_atual, "chromedriver-win64", "chromedriver.exe")
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://github.com/login")
  

   
def login_site(login, senha):
    try:
        # Aguarda até que o campo de login esteja presente
        user_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login_field"]'))
            )
        user_field.send_keys(login)

        # Aguarda até que o campo de senha esteja presente
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
            )
        password_field.send_keys(senha)
        
        # Clica no botão de login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@name="commit"]'))
            )
        login_button.click()
        
        # Aguarda a presença do elemento que indica um erro de login
        error_element_present = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-flash-container"]/div/div/div'))
                )
        # Se o elemento de erro estiver presente, limpa os campos
        if error_element_present:
            close_error = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="js-flash-container"]/div/div/button/svg'))
                )
            close_error.click()
            user_field.clear()
            password_field.clear()
            messagebox.showerror("Erro", "Erro ao tentar logar: credenciais inválidas")
            return False
        
        # Aguarda a presença de um elemento que só aparece após o login bem-sucedido
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Your repositories")]'))
        )
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        return True
    except Exception as e:
        messagebox.showerror("Erro", "Erro ao tentar logar: " + str(e))
        return False   



def submit_login():
    login = login_entry.get()
    senha = senha_entry.get()

    if login and senha:
        if login_site(login, senha):
            root.destroy()  # Fecha a janela de login se o login for bem-sucedido
        else:
            login_entry.delete(0, tk.END)  # Limpa o campo de login
            senha_entry.delete(0, tk.END)  # Limpa o campo de senha
            messagebox.showwarning("Aviso", "Por favor, insira os dados novamente")
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha os campos de login e senha.")

# Cria a janela principal com tkinter
root = tk.Tk()
root.title("Tela de Login")

# Widgets de entrada para login e senha
login_label = tk.Label(root, text="Login:")
login_label.grid(row=0, column=0, padx=25, pady=10)

login_entry = tk.Entry(root, width=30)
login_entry.grid(row=0, column=1, padx=25, pady=10)

senha_label = tk.Label(root, text="Senha:")
senha_label.grid(row=1, column=0, padx=25, pady=10)

senha_entry = tk.Entry(root, show='*', width=30)
senha_entry.grid(row=1, column=1, padx=25, pady=10)

# Botão para submeter o login
submit_button = tk.Button(root, text="Login", command=submit_login)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Seleciona automaticamente o campo de login ao abrir a janela
login_entry.focus_set()

# Inicia o loop principal do tkinter
root.mainloop()