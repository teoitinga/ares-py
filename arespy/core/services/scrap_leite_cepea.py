import requests
import pandas as pd
import xlrd
import locale

class Cepea:
    link_leite = 'https://www.cepea.esalq.usp.br/br/indicador/series/leite.aspx?id=leitep'
    link_boi = 'https://www.cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2'
    link_bezerro = 'https://www.cepea.esalq.usp.br/br/indicador/series/bezerro-media-sao-paulo.aspx?id=3'
    link_peso_bezerro = 'https://www.cepea.esalq.usp.br/br/indicador/series/bezerro.aspx?id=174'
    link_milho = 'https://www.cepea.esalq.usp.br/br/indicador/series/milho.aspx?id=77'
    link_cafe_arabica = 'https://www.cepea.esalq.usp.br/br/indicador/series/cafe.aspx?id=23'
    link_cafe_robusta = 'https://www.cepea.esalq.usp.br/br/indicador/series/cafe.aspx?id=24'

    #Define o local onde serão armazenadas as planilhas, posteriormente, definir em variável ambiente
    path = './core/datasets/'#'./datasets/'
    ext = '.xls'

    file_leite = path + 'cepea_leite' + ext
    file_boi = path + 'cepea_boi' + ext
    file_bezerro = path + 'cepea_bezerro' + ext
    file_peso_bezerro = path + 'cepea_peso_bezerro' + ext
    file_milho = path + 'cepea_milho' + ext
    file_cafe_arabica = path + 'cepea_cafe_arabica' + ext
    file_cafe_robusta = path + 'cepea_cafe_robusta' + ext

    #Converte o mes por extenso em número de 1 a 12
    def convmonth(sgl):
        if sgl=='JAN':
            return 1
        if sgl=='FEV':
            return 2
        if sgl=='MAR':
            return 3
        if sgl=='ABR':
            return 4
        if sgl=='MAI':
            return 5
        if sgl=='JUN':
            return 6
        if sgl=='JUL':
            return 7
        if sgl=='AGO':
            return 8
        if sgl=='SET':
            return 9
        if sgl=='OUT':
            return 10
        if sgl=='NOV':
            return 11
        if sgl=='DEZ':
            return 12

    #Baixa novamente as planilhas diretamente do site CEPEA
    def update_all_tables():
        #Cepea.tbl_bezerro()
        #Cepea.tbl_boi_gordo()
        #Cepea.tbl_cafe_arabica()
        #Cepea.tbl_cafe_robusta()
        Cepea.tbl_leite()
        #Cepea.tbl_milho()

    #Recarrega os dados das planilhas já baixadas e armazena nas variáveis que estão ativas
    def reload_all_tables():
        #Reload Cepea data
        Cepea.load_leite()
        #Cepea.load_bezerro()
        #Cepea.load_peso_bezerro()
        #Cepea.load_boi_gordo()
        #Cepea.load_milho()
        #Cepea.load_cafe_arabica()
        #Cepea.load_cafe_robusta()

    def media_anual_leite():
        m_anual = Cepea.df_leite.groupby(pd.Grouper(key='DATA', freq='1A')).agg({'Valor_R$':'mean'})
        m_anual['Ano'] = m_anual.index.year
        response = m_anual.to_json(orient='table', index=False) 
        return response

    def atual_prices():
        dados = []

        #Leite
        row = {}
        reg = Cepea.df_leite.sort_values('DATA', ascending=False).head(1)
        row['data'] = reg.iloc[0]['DATA'].strftime('%Y-%m-%d')
        row['producao'] = 'Leite MG'
        row['unidade'] = 'lt'
        row['valor'] = reg.iloc[0]['Valor_R$']
        row['coments'] = '*fonte CEPEA MG - link: https://www.cepea.esalq.usp.br/br/indicador/leite.aspx'
        dados.append(row)

        response = pd.DataFrame(dados).to_json(orient='table', index=False) 
        return response

    def request_save(link, header, file):
        file_name = file
        resp = requests.get(link, headers=header)
        output = open(file_name, 'wb')
        output.write(resp.content)
        output.close()

    def tbl_leite():

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=58gh7usd6rgmcnhevdndg89rh2; _ga=GA1.2.308146475.1648922473; _hjSessionUser_1853339=eyJpZCI6ImMwNWI2OTg5LTc5MWItNWQyZS04NzIxLWJjNjRjNWE1MjFjYiIsImNyZWF0ZWQiOjE2NDg5MjI0NzM2OTksImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.2062172903.1651950311; _gat=1; _gat_UA-169211747-1=1; _hjIncludedInPageviewSample=1; _hjSession_1853339=eyJpZCI6IjgwMjcxNGVlLTUwMTktNDc4ZS1hNjQzLWJkNmM5MTI3M2FkNyIsImNyZWF0ZWQiOjE2NTE5NTAzMTE1MTcsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0',
            'Host': 'www.cepea.esalq.usp.br',
            'Referer': 'https://www.cepea.esalq.usp.br/br/indicador/leite.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"'
            }
        link = Cepea.link_leite
        file_name = Cepea.file_leite

        #Baixa a planilha e salva na pasta definida
        Cepea.request_save(link, header, file_name)
        #Atualliza as variáveis com os novos dados
        Cepea.load_leite()

    def load_leite():
        workbook = xlrd.open_workbook_xls(Cepea.file_leite , ignore_workbook_corruption=True)
        dados = pd.read_excel(workbook)
        columns = ['ANO', 'MES', 'UF', 'Valor_R$']#'Valor_MIN_R$', 'Valor_R$']
        dados  = pd.DataFrame(dados.values[4:, 0:5], columns=columns)
        dados['MES'] = dados['MES'].apply(Cepea.convmonth)
        dados['DATA'] = dados['ANO'].astype(str)+ '-'+ dados['MES'].astype(str)
        dados['DATA'] = pd.to_datetime(dados['DATA'], format='%Y-%m')
        dados['Valor_R$'] = dados['Valor_R$'].astype(str).astype(float)
        dados_leite = dados[dados['UF']=='MG'][['DATA', 'Valor_R$' ]]
        Cepea.df_leite = dados_leite

