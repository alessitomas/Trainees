import pyautogui
from datetime import datetime
import time

lista_itens = ['kindle 10h Generation']

screenWidth, screenHeight = pyautogui.size() # Função que vai retornar o tamanho da minha tela
print(screenWidth, screenHeight )

pyautogui.press('win') # Farei o Pc apretar a tecla do iniciar
time.sleep(2)
pyautogui.write('Google Chrome', interval=0.01) # Escreverei 'Google Chrome' para pesquisar o navegador que eu quero abrir
pyautogui.press('ENTER') # Abrirei o Chrome
time.sleep(2) #Irei esperar o Chrome abrir

pyautogui.press('f11') # Farei o Chrome ficar em tela cheia para facilitar
pyautogui.moveTo(643, 522)
pyautogui.click()

time.sleep(2)
pyautogui.write('www.amazon.com.br', interval=0.01)
pyautogui.press('ENTER')
time.sleep(2)

for item in lista_itens:
    pyautogui.moveTo(776, 46)
    pyautogui.click(clicks=3)
    pyautogui.press('delete')

    time.sleep(2)
    pyautogui.write(item, interval=0.01)
    pyautogui.press('ENTER')
    time.sleep(2)

    pyautogui.moveTo(627, 492)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(1056, 281)
    pyautogui.click(clicks=3)
    pyautogui.hotkey('ctrl', 'c') #Aqui eu estarei copiando a informação com o Ctrl c
    time.sleep(2)

    if lista_itens.index(item) == 0:
        pyautogui.press('win')
        time.sleep(2)
        pyautogui.write('C:\\Users\spedr\Desktop\Cases-trainees\Aula-WebScrapping\Excel.xlsx', interval=0.01) # Substituam pelo path do excel de vocês
        pyautogui.press('ENTER')
        time.sleep(5)
    else:
        pyautogui.hotkey('alt', 'tab')


    pyautogui.moveTo(30, 385)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.moveTo(95, 690)
    pyautogui.click()

    pyautogui.moveTo(85, 380)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'v') #Aqui eu estarei copiando a informação com o Ctrl c
    pyautogui.hotkey('ctrl', 'b') #Aqui eu estarei salvando o Excel

    pyautogui.hotkey('alt', 'tab')
    pyautogui.moveTo(1042, 664)
    pyautogui.click(clicks=2)
    pyautogui.hotkey('ctrl', 'c') #Aqui eu estarei copiando a informação com o Ctrl c
    time.sleep(2)

    pyautogui.hotkey('alt', 'tab')

    pyautogui.moveTo(220, 380)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'v') #Aqui eu estarei copiando a informação com o Ctrl c
    pyautogui.hotkey('ctrl', 'b') #Aqui eu estarei salvando o Excel

    pyautogui.moveTo(340, 380)
    pyautogui.click()
    data = datetime.now().strftime('%d/%m/%Y')
    pyautogui.write(data, interval=0.1)
    pyautogui.hotkey('ctrl', 'b') #Aqui eu estarei salvando o Excel
    pyautogui.hotkey('alt', 'tab')


# #Aqui eu estarei fechando o chrome e o excel
time.sleep(3)
pyautogui.click()
pyautogui.hotkey('ctrl', 'w') 
time.sleep(3)
pyautogui.moveTo(1883, 22)
pyautogui.click()


#Apartir deste ponto eu farei a exportação dos dados
import os
import json
import pandas as pd
import gspread
import gspread_dataframe as gd
from dotenv import load_dotenv, find_dotenv

# Extraindo variaveis do .env
load_dotenv(find_dotenv())

credentials = json.loads(os.getenv('credentials'))
wks_name = os.getenv('wks_name')
login_usuario = os.getenv('login')
senha_usuario = os.getenv('senha')

#Aqui eu estarei trazendo o execel para o código em python
df = pd.read_excel('Excel.xlsx')
# Set up conexão com google sheets
gc = gspread.service_account_from_dict(credentials)
sheets = gc.open(wks_name) # Aqui ele abrira o sheets que vocês criaram

worksheet = 'AutoGui' #Mudem para o nome da página do sheets que vocês criaram no sheets

# Abrindo a tab correspondente
tab = sheets.worksheet(worksheet)

Infos = gd.get_as_dataframe(tab) #Extraindo as informações que já estavam no dataframe
updated_duplicated = pd.concat([Infos, df], ignore_index=True)
gd.set_with_dataframe(tab, updated_duplicated)

# Link para o meu sheets
# https://docs.google.com/spreadsheets/d/1682T49um_1PrMIQP4ScX9ElOq9q8ckrweg_KAYKkubQ/edit?usp=sharing