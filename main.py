from threading import local
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
import locale
from modelos import Estrategia, FundoImobiliario

locale.setlocale(locale.LC_ALL, 'pt-BR.UTF-8')

def tratar_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split("%")[0])

def tratar_decimal(decimal_str):
    return locale.atof(decimal_str)

estrategia = Estrategia(cotacao_minima = 60, 
qt_imoveis_minima = 5, 
dividend_yield_minima = 0.5, 
valor_mercado_minimo = 40000,
liquidez_minima = 100000)

resultado = []

headers = {'User-Agent': 'Mozilla/5.0'}

resposta = requests.get('http://www.fundamentus.com.br/fii_resultado.php', headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')

linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')
for linha in linhas:
    dados_fundo = linha.find_all('td')
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao_atual = tratar_decimal(dados_fundo[2].text)
    ffo_yield = tratar_porcentagem(dados_fundo[3].text)
    dividend_yield = tratar_porcentagem(dados_fundo[4].text)
    p_vp = tratar_decimal(dados_fundo[5].text)
    valor_mercado = tratar_decimal(dados_fundo[6].text)
    liquidez = tratar_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = tratar_decimal(dados_fundo[9].text)
    aluguel_m2 = tratar_decimal(dados_fundo[10].text)
    cap_rate = tratar_porcentagem(dados_fundo[11].text)
    vacancia_med = tratar_porcentagem(dados_fundo[12].text)

    fundo_imobiliario = FundoImobiliario(codigo, segmento, cotacao_atual, ffo_yield, dividend_yield, p_vp, valor_mercado, liquidez, qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_med)
    if estrategia.aplicar_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)

cabecalho = ["CÓDIGO", "SEGMENTO", "COTAÇÃO", "CAP RATE"]
tabela = []

for elemento in resultado:
    tabela.append([elemento.codigo, elemento.segmento, elemento.cotacao_atual, locale.str(elemento.cap_rate)])

print(tabulate(tabela, headers=cabecalho, tablefmt = "fancy_grid", showindex="always"))