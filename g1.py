import requests
from bs4 import BeautifulSoup
import pandas as pd

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
s = requests.Session()
s.headers.update(headers)



#categorias = ['ciencia', 'mundo', 'politica', 'saude', 'tecnologia', 'esporte', 'religiao', 'entretenimento']

# apenas categorias com correspondencia no g1
categorias = ['ciencia', 'mundo', 'politica', 'saude', 'tecnologia']


qtd = 5000
item_por_pagina = 10
qtd_por_cat = int(qtd / len(categorias))
pagina_por_cat = int(qtd_por_cat / item_por_pagina)

dataset = []
for c in categorias:
    for x in range(0, pagina_por_cat): 
        print(f'Página {x} de {pagina_por_cat} da categoria {c}')
        s = requests.Session()
        s.headers.update(headers)
        r = s.get(f'https://g1.globo.com/{c}/index/feed/pagina-{x}.ghtml', headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        noticias = soup.findAll('div', attrs={'class': 'feed-post-body'})
        
        for n in noticias:
            titulo = n.find('div', attrs={'class': 'feed-post-body-title'})
            categoria = n.find('span', attrs={'class': 'feed-post-metadata-section'})    
            resumo = n.find('div', attrs={'class': 'feed-post-body-resumo'})
            
            link = titulo.find('a')
            link = link['href']
            # print(link)

            if(resumo):
                resumo = resumo.text
            else:
                resumo = 'Erro'

            # r = s.get(f'{link}', headers=headers)
            # artigo = BeautifulSoup(r.text, 'html.parser')
            # data = artigo.find('time')
            
            # if(data):
            #     data = data.text
            # else:
            #     data = 'Erro'
            # print(data)
            # data = n.find('span', attrs={'class': 'feed-post-datetime'})
            # dataset.append([titulo.text, categoria.text if categoria else 'Nenhum', resumo, data, 'Verdadeira'])

            dataset.append([titulo.text, categoria.text if categoria else 'Nenhum', resumo, 'Verdadeira'])

print(f'\nTotal de registros salvos: {len(dataset)}')

df = pd.DataFrame(dataset, columns=['Titulo', 'Categoria', 'Resumo', 'Status'])

df.to_csv('verdadeiras.csv', index=False)
