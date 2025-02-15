from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


URL = "https://www.ivannegocios.com.br/alugar/Uberlandia/Casa"

response = requests.get(URL)
time.sleep(10)
data = response.text
soup = BeautifulSoup(data, 'html.parser')


bairros = soup.select('p.card-bairro-cidade')
todos_bairros = [bairro.text.split(' - ')[0] for bairro in bairros]


precos = soup.select('div.card-valores')
todos_precos = [preco.text.strip().replace("R$", "").replace(".", "").replace("L", "") for preco in precos]


#transformar os dados coletados em data frame no pandas
dados = pd.DataFrame({
    'Bairro': todos_bairros,
    'precos': todos_precos
})


def tratar_precos(preco):
    '''essa funcao foi criada para podermos tratar os precos, pois em alguns dados temos precos para alugel e venda,
    alem de precos com desconto.'''

    precos = preco.replace("\n", "").split() #divide os precos que contêm 'dois precos'

    if 'V' in preco: # se tiver preco de venda retorna o preco de aluguel.
        return preco[0]

    return min(float(p.replace(',', '.')) for p in precos) # se tiver preco de alguel com desconto ele retorna o menor preco

dados['precos'] = dados['precos'].apply(tratar_precos) # retorna os valores de precos tratados.

dados.to_csv('alugueis_uberlandia.csv',index=True) # exporta para csv para analisarmos o dados.









