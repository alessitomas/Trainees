# Importando Bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
from rich.console import Console
from rich.table import Table

# Extraindo variaveis do .env
load_dotenv(find_dotenv())

login_usuario = os.getenv('login')
senha_usuario = os.getenv('senha')

# Set Up Chrome driver
chrome_options = Options() #Opções de inicialização do Chrome

# chrome_options.add_argument("--incognito")            # Abre a navegação anonima
chrome_options.add_argument("--headless")             # Esconde a interface gráfica tornando o driver muito mais rápido
# chrome_options.add_argument("no-sandbox")             # Desativa a segurança de alguns sites que bloqueiam o headless
# chrome_options.add_argument("--window-size=800,600")  # Abre a janela no tamanho desejado (em pixels)
# chrome_options.add_argument("--window-size=800,600")  # Abre a janela no tamanho desejado (em pixels)

#Inicializando Driver
# ChromeDriverManager().install(): Esse comando instalará o driver diretamente no seu computador
# chrome_options=chrome_options : Esse comando fará as opções de inicialização serem aplicadas
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

url = 'https://www.amazon.com.br'
driver.get(url=url)

#Realizando Login
login = driver.find_element(By.XPATH, '//*[@id="nav-link-accountList"]') #Definição do elemento a partir do driver (driver.find_element) pelo Xpath que está sendo encontrado apartir do id
login.click()

driver.implicitly_wait(time_to_wait=5) #Função para fazer o driver esperar a página como um todo carregar

input_login = driver.find_element(By.ID, 'ap_email') # Indicar onde daremos o input do login
input_login.send_keys(login_usuario) # Enviar o texto para o objeto de input

button_confirm = driver.find_element(By.XPATH, '//*[@id="continue"]') #Lembrando que não existe diferença entre essa linha e a proxima
# button_confirm = driver.find_element(By.ID, 'continue')
button_confirm.click()

driver.implicitly_wait(time_to_wait=5)

input_senha = driver.find_element(By.ID, 'ap_password')
input_senha.send_keys(senha_usuario)

button_confirm = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')
button_confirm.click()

driver.implicitly_wait(time_to_wait=5)

#Entendo na Lista de desejos
actions = ActionChains(driver) # Função que indica que vamos querer inicializar a biblioteca de ações na página atual do driver

menu_options = driver.find_element(By.XPATH, '//*[@id="nav-link-accountList"]')
actions.move_to_element(menu_options).perform() #Essa ação fara que um mouse simulado se locomova até o objeto

my_wishlist = driver.find_element(By.XPATH, '//*[@id="nav-al-your-account"]/a[3]') # Uma vantagem de usar o XPATH, eu posso fazer com que o driver ache o um objeto pelo id e mas me devolva um item dentro dele (nesse caso o item é o "a[3]")
my_wishlist.click()

driver.implicitly_wait(time_to_wait=5)

enter_list = driver.find_element(By.ID, 'wl-list-entry-title-1NKNN4MF7E8XW')
enter_list.click()

driver.implicitly_wait(time_to_wait=5)

actions = ActionChains(driver) # Eu refiz o actions porque a página mudou de layout, então é necessário refazer a ação

fim = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/div[8]/div/div/div[3]/div/div/span/h3')
actions.move_to_element(fim).perform() #Como nem todos os elementos são carregado quando a página é aberta eu irei força-los a serem carregados, movendo a tela até um ponto após a lista (o move_to_element tem a liberdade de mover o scroll)
time.sleep(2)

itens = driver.find_elements(By.XPATH, '//*[@data-id="1NKNN4MF7E8XW"]') # Essa e a próximas são basicamente a mesma coisa, mas esta eu percebi que existia um elemento na tag que se repetia para todos os itens +
# itens = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/div[8]/div/div/ul/li') # + Enquanto essa eu peguei o Xpath de um item e tirei a indicação de index que existia no fim (ex: ...ul/li[4])
itens_achados = len(itens)
itens_na_lista = 0

#Inicializando uma tabela
table = Table(title="Produtos") 
# Aqui eu vou fazer a inicialização da estrutura de tabela com o rich, usem isso como eu tinha falado, apenas para teste,
# quando a estrutura em dataframe estiver pronta retirem tudo correlacionado, pois apenas irá poluir o código

#Criando suas colunas da table
table.add_column("Nome", justify="left", style="white")
table.add_column("Preço", justify="center", style="magenta")
table.add_column("Nº Avaliações", justify="center", style="magenta")
table.add_column("Nota", justify="center", style="magenta")
table.add_column("Tempo", justify="center", style="magenta")


for item in itens:
    # Nesse ponto esse código será aplicado em cada item
    # Para extrair cada informação nós normalmente precisamos pegar o valor de texto dentro da tag Ex: <a>Kindle</a> para extrair esse valor é usado o .text que devolverá a string "Kindle"
    nome_item = item.find_element(By.XPATH, "span/div/div/div/div[2]/div[3]/div/div[1]/div/div[1]/div[1]/h2/a").text

    reais = item.find_element(By.CLASS_NAME, 'a-price-whole').text.replace(",", ".")
    cents = item.find_element(By.CLASS_NAME, 'a-price-fraction').text
    preço = float(reais+cents)

    n_avaliaçoes = item.find_element(By.XPATH, 'span/div/div/div/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div[1]/a[2]').text
    n_avaliaçoes = n_avaliaçoes.replace('.','')

    estrelas = item.find_element(By.XPATH, 'span/div/div/div/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div[1]/span/a').get_attribute('aria-label') 
    # Nesse caso em específico eu não estrai o valor do texto, mas o valor de um dos atributos do elemento Ex: <a aria-label="4.9">Kindle</a>, nesse caso eu quero a nota da avaliação, então o .text não me serve, mas a minha informação está no atributo aria-label, então por isso essa função
    avaliaçao = estrelas.replace(' de 5 estrelas', '')

    tempo = item.find_element(By.XPATH, '//*[@id="itemAddedDate_I2I7UC8RDIEEKR"]').text

    # Adicionando as linhas ao rich
    table.add_row(str(nome_item), "R$ {0:.2f}".format(preço), n_avaliaçoes, avaliaçao, tempo)

# Criando e mostrando a tabela
console = Console().print(table)

# Fechando o driver
driver.close()