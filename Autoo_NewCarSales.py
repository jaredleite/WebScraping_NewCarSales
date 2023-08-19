import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd


ano = 2009


arq = os.getcwd() + f'\\Autoo_NewCarSales_{ano}.csv'

options = Options()
options.add_argument('window-size=400,800')
# options.add_argument('--headless')

frames = []


def get_table(table):
    global frames

    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
    table_headers = []
    for th in soup.find_all('th'):
        table_headers.append(th.text.replace('\n', ''))

    table_data = []
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text.replace('\n', ''))
        table_data.append(output_row)

    df = pd.DataFrame(table_data, columns=table_headers)
    # print(df)
    frames.append(df)
    # return df


navegador = webdriver.Chrome(options=options)
navegador.get(
    f'https://www.autoo.com.br/emplacamentos/veiculos-mais-vendidos/{ano}/')
sleep(5)

input_select_example_length = Select(
    navegador.find_element(By.NAME, 'example_length'))
input_select_example_length.select_by_visible_text("20")
sleep(5)

# //*[@id="example_paginate"]/span
last_page = int(navegador.find_elements(
    By.CLASS_NAME, 'paginate_button ')[-2].text)


print(f'Last page: {last_page}')
#                             ).find_elements(By.CLASS_NAME, 'paginate_button'))

next_button = navegador.find_element(By.ID, 'example_next')

table = navegador.find_element(By.ID, 'example')

for i in range(last_page):
    table = navegador.find_element(By.ID, 'example')
    get_table(table)

    next_button.click()
    sleep(5)

    next_button = navegador.find_element(By.ID, 'example_next')

df = pd.concat(frames)
print(df)

df.to_csv(arq, index=False, encoding='utf-8')
