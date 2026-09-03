" ======================================================================="
" ====================== REGISTRO DE MANUTENÇÃO ========================="
" ======================================================================="


"""
=============================================================
Projeto         : Automação SAP
Arquivo         : logger.py

Criado por      : GUSTAVO ALMEIDA HERMOGENES
Data Criação    : --------

Última Alteração
-------------------------------------------------------------
User            : Z701038
Dev             : Tiago Eneas Antunes
Data            : 01/09/2026
Hora            : 08:56

Descrição       : Limpeza de dados.
=============================================================
"""

" ======================================================================="
" ====================== BIBLIOTECAS PRINCIPAIS ========================="
" ======================================================================="


import pandas as pd
import datetime
import os
import numpy as np


" ======================================================================="
" ========================= FUNÇÕES AUXILIARES =========================="
" ======================================================================="


# Função para ler o excel e transformar em DataFrame
def excel_para_df(caminho:str):
    try:

        df = pd.read_excel(caminho, decimal=',', thousands='.')
        return df
    
    except Exception as e:
        print(f'Erro função excel_para_df: {e}')

# Função para limpar e tratar os dados do DataFrame
def transformar_df(df: pd.DataFrame):
    try:
        # Encontra a primeira linha que contenha dados válidos
        df = df.iloc[df['Unnamed: 2'].first_valid_index():].reset_index(drop=True)

        nomes_colunas = df.loc[0].to_list()
        df.columns = nomes_colunas

        df = df.drop(axis=0, index=0)

        df = df.dropna(how='all')


        df = df.dropna(axis=1, how='all')


        df = df[df['Doc.compra'] != 'Doc.compra']
        
        df = df[
            df['Doc.compra'].notna() &
            df['Doc.compra'].astype(str).str.strip().str.isdigit()
        ]

        df = df.loc[:, ~df.columns.duplicated()]


        df = df.rename(columns={
                    'Fornecedor' : 'Cod. Fornecedor',
                    'Nº conta do fornecedor' : 'Nome Fornecedor',
                    ' Doc.compra' : 'Doc.compra'
                })
        
        for col in ['Data doc.', 'Dt.remessa']:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .where(df[col].notna())
                .apply(lambda x: f'{x[0:2]}/{x[2:4]}/{x[4:8]}' if len(x) == 8 else x)
            )

        df['Itm'] = df['Itm'].astype(str).str.lstrip('0')
        df['Doc.compra'] = df['Doc.compra'].astype(str).str.lstrip('0')

        df['PO'] = df['Doc.compra'] + df['Itm']

        colunas = ['PO'] + [col for col in df.columns if col != 'PO']
        df = df[colunas]

        df = df.sort_values(by='PO', ascending=False)

        df['Valor efetivo'] = df['Valor efetivo'].astype(float)
        df['VAL PEND EF'] = df['VAL PEND EF'].astype(float)

        df['Valor efetivo'] = df.apply(
                    lambda x: x['Valor efetivo'] * 1.5 * 5.6 if x['Moeda'] == 'USD' else x['Valor efetivo'],
                    axis=1
                )

        df['VAL PEND EF'] = df.apply(
                    lambda x: x['VAL PEND EF'] * 1.5 * 5.6 if x['Moeda'] == 'USD' else x['VAL PEND EF'],
                    axis=1
                )
        
 
        return df
    
    except Exception as e:
        raise Exception(f'Erro função transformar_df: {e}')

def concatenar_fups(df1: pd.DataFrame, df2: pd.DataFrame):
    try:
        # Concatena os 2 DataFrames referentes ao FUP de acordo com as linhas
        df_concatenado = pd.concat([df1, df2], axis=0)

        # Remove duplicatas
        df_concatenado.drop_duplicates('PO', keep='last', inplace=True)

        # Ordena o DataFrame de forma decrescente
        df_concatenado.sort_values(by='PO', ascending=False, inplace=True)
        
        lista_projetos_especiais = [
            'EI.25017.01',
            'EI.25016.71',
            'EI.25016.01',
            'EI.25016.59',
            'EI.25016.50',
            'EI.25016.78',
            'EI.26016.03', 
            'EI.26016.83',
            'EI.26016.17',
            'EI.26016.15',
            'EI.26016.11',
            'EP.26500.01'
        ]

        df_concatenado = df_concatenado[~df_concatenado['ElementoPep'].str.slice(0, 11).isin(lista_projetos_especiais)]

        return df_concatenado
    
    except Exception as e:
        print(f'Erro: {e}')

def concatenar_estoques(df1: pd.DataFrame, df2: pd.DataFrame):
    try:
        # Concatena os 2 DataFrames referentes de acordo com as linhas
        df_concatenado = pd.concat([df1, df2], axis=0)

        df_concatenado = df_concatenado[['Material', 'Texto breve material', 'TMat', 'Cen.', 'Dep.', 'Utilização livre', 'Elemento PEP', 'Moeda', 'Val.utiliz.livre', 'Denominação', 'Unid./Negocio']]
        df_concatenado['Ano PEP'] = df_concatenado['Elemento PEP'].apply(
            lambda x: '20' + x[3:5] if x != '-' else '-'
        )

        return df_concatenado
    
    except Exception as e:
        print(f'Erro: {e}')

def transformar_pedidos_compras(caminho_arquivo : str):
    try:
        df = pd.read_excel(caminho_arquivo)

        # Remove a coluna ITEM da req. para não confundir com o do pedido
        df.drop(columns=['Unnamed: 2'], inplace= True)
        
        # Encontra a linha que contém os primeiros registros válidos
        primeiro_index = df['Unnamed: 1'].first_valid_index()

        # Filtra do primeiro indice válido até o final, resetando o index e excluindo o antigo
        df = df.loc[primeiro_index:].reset_index(drop=True)

        # Definindo o cabeçalho da tabela a partir da primeira linha (onde estavam localizados)
        nomes_colunas = df.loc[0].to_list()
        df.columns = nomes_colunas

        # Definindo as colunas importantes
        df = df[['ReqC','Pedido', 'Item', 'Requis.', 'DataConf.']]

        # Observando os últimos registros válidos
        ultimo_index = df.last_valid_index()
        df = df.iloc[2:ultimo_index]

        df.dropna(how='all', inplace=True)
        
        # Filtrando as datas (a partir de 1 mês atrás)
        hoje = datetime.datetime.today()
        data_anterior = hoje - datetime.timedelta(days=30)
        hoje = hoje.strftime("%d/%m/%Y")
        data_anterior = data_anterior.strftime("%d/%m/%Y")

        df['DataConf.'] = pd.to_datetime(df['DataConf.'], format= '%d.%m.%Y')

        df['DataConf.'].dt.strftime("%d/%m/%Y")

        df = df[df['DataConf.'] >= data_anterior]

        # Retirando os pedidos que começam com 55
        df = df[~df['Pedido'].astype(str).str.startswith('55')]

        # Retirando os pedidos especiais
        df = df[~(df['Requis.'].str.endswith('ESPECI') | df['Requis.'].str.endswith('ESPCI') | df['Requis.'].str.endswith('ESPECIA') | df['Requis.'].str.endswith('ESPECIAIS') | df['Requis.'].str.endswith('ESPECIAL') | df['Requis.'].str.endswith('ESPECIAS') | df['Requis.'].str.endswith('ESPECIAOS'))]

        # Filtrando as colunas necessárias
        df = df[['Pedido', 'Item']]

        return df

    except Exception as e:
        print(f'Erro na função transformar_pedidos_compras! {e}')

# Função criada para retornar o diretório de um determinado arquivo
def retorna_caminho(nome_arquivo:str, caminho_pasta:str):
    try:
        arquivos = os.listdir(caminho_pasta)

        for i in arquivos:
           if i.startswith(nome_arquivo) and i.endswith('.xlsx'):
                caminho = os.path.join(caminho_pasta, i)
                return caminho.replace("\\", "\\\\")
                
    except Exception as e:
        print(f'Verifique se o diretório informado ou se o nome do arquivo são válidos:\n{e}')

def df_para_excel(df: pd.DataFrame, caminho_pasta:str, nome_arquivo:str):
    try:
        caminho_completo = f'{caminho_pasta}\{nome_arquivo}'
        df.to_excel(f'{caminho_completo}.xlsx', index=False)
        print(f'Excel carregado com Sucesso!\nCaminho: {caminho_completo}')
    except Exception as e:
        print(f'Erro função df_para_excel: {e}')