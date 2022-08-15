import requests
from bs4 import BeautifulSoup
import pandas as pd

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
s = requests.Session()
s.headers.update(headers)


# apenas categorias com correspondencia no g1
categorias = ['ciencia', 'mundo', 'politica', 'saude', 'tecnologia']

qtd = 5000
item_por_pagina = 50
qtd_por_cat = int(qtd / len(categorias))
pagina_por_cat = int(qtd_por_cat / item_por_pagina)



dataset = []
for categoria in categorias:
    for x in range(0, pagina_por_cat):
        print(f'Página {x} de {pagina_por_cat} da categoria {categoria}')
        r = s.get(f'https://www.boatos.org/{categoria}/feed?paged={x}', headers=headers)
        soup = BeautifulSoup(r.text, 'lxml-xml')
        
        itens = soup.findAll('item')

        for item in itens:
            link = item.find('link')
            link = link.text
            # print(link)
            r = s.get(f'{link}', headers=headers)
            artigo = BeautifulSoup(r.text, 'html.parser')

            titulo = artigo.find('h1', attrs={'class': 'entry-title'})
            titulo = titulo.text.replace('#boato', '')
            titulo = titulo.replace('boato', '')
            titulo = titulo.replace('Mentira:', '')
            titulo = titulo.replace('Pegadinha:', '')
            # print(titulo)

            resumo = artigo.select('div.entry-content > p:nth-of-type(1) > strong')
        
            if(resumo):
                pass
            else:
                resumo = artigo.select('div.entry-content > p:nth-child(2) > b')
                if(resumo):
                    pass
                else:
                    resumo = artigo.select('div.entry-content > p:nth-child(2)')
                    if(resumo):
                        pass
                    else: 
                        resumo = artigo.select('div.entry-content > p:nth-child(3)')
                        if(resumo):
                            pass
                        else:
                            resumo = artigo.select('div.entry-content > div:nth-child(1) > p')
                        if(resumo):
                                pass
                        else:
                                print(link)

            
            resumo = resumo[0].text.replace('Boato – ', '')


            data = artigo.find('time', attrs={'class': 'published'})
            data = data.text

            dataset.append([titulo, categoria, resumo, data, 'Falsa'])


print(f'\nTotal de registros salvos: {len(dataset)}')


df = pd.DataFrame(dataset, columns=['Titulo', 'Categoria', 'Resumo', 'Data', 'Status'])

# print(df)

df.to_csv('falsas.csv', index=False)

