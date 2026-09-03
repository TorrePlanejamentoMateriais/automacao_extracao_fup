" ======================================================================="
" ====================== REGISTRO DE MANUTENÇÃO ========================="
" ======================================================================="


"""
=============================================================
Projeto         : Automação SAP
Arquivo         : logger.py

Criado por      : GUSTAVO ALMEIDA HERMOGENES
Data Criação    : -------
Última Alteração
-------------------------------------------------------------
User            : Z701038
Dev             : Tiago Eneas Antunes
Data            : 01/09/2026
Hora            : 08:56

Descrição       : Funções que contém funcionalidades para a automação.
=============================================================
"""

" ======================================================================="
" ====================== BIBLIOTECAS PRINCIPAIS ========================="
" ======================================================================="

import pandas as pd
import pyautogui
import time
import datetime
import sys
import os
import pyperclip

" ======================================================================="
" ====================== FUNÇÕES AUXILIARES ============================="
" ======================================================================="

from utils.limpeza_dados import df_para_excel
from utils.logger import logger
from utils.posicoes import Posicoes
from classes.monitor import MonitorExecucao


" ======================================================================="
" ====================== FUNÇÕES AUTOMAÇÃO FUP/SAP ======================"
" ======================================================================="

# Classe que irá monitorar total de execuções e erro
monitor = MonitorExecucao()
posicoes = Posicoes()

#Classe que contém as Posições

# Função criada para retornar o diretório de um determinado arquivo
def retorna_caminho(nome_arquivo:str, caminho_pasta:str):
    try:
        arquivos = os.listdir(caminho_pasta)
        
        if nome_arquivo.upper() == 'FUP' or nome_arquivo.startswith('Protocolos') or nome_arquivo.startswith('Pedidos de Compras'):
            caminho = ''
            for i in arquivos:
                if i.startswith(nome_arquivo) and i.endswith('.xlsx'):
                    caminho = os.path.join(caminho_pasta, i)
                    return caminho.replace("\\", "\\\\")

        else:
            caminho_imagem = ''
            for i in os.listdir(caminho_pasta):
                if i.startswith(nome_arquivo) and i.endswith('.png'):
                    caminho_imagem = os.path.join(caminho_pasta, i)
                    return caminho_imagem.replace("\\", "\\\\")
                
    except Exception as e:

        monitor.registrar_excecao(
            "retorna_caminho",
            str(e)
        )

        logger.error(f'Verifique se o diretório informado ou se o nome do arquivo são válidos:\n{e}')

caminho_fup_atual = retorna_caminho('FUP', caminho_pasta_fup)

# Função para simular um menu de opções de extrações no SAP
def menu():
    try:
        opcao_selecionada = int(input(
            "Escolha o tipo de extração:\n[1] FUP atualização base atual\n[2] FUP novos pedidos\n[3] Pedido de Compras\n[4] Protocolos\n[5] Agendamentos\n[6] Estoque Empresarial\n[7] Estoque Residencial\n"))

    except Exception as e:

        monitor.registrar_excecao(
            "menu_opção_inválida",
            str(e)
        )

        logger.error(f'Por favor, selecione uma opção válida. Erro:\n{e}')

    return opcao_selecionada

def aguarda_imagem(nome_imagem: str, confidence=0.7, timeout=60):
    # Garante que não vai lançar exceção
    logger.info("Aguardando a imagem:", nome_imagem)
    pyautogui.useImageNotFoundException(False)

    # Obtendo o caminho completo da imagem
    caminho_completo = os.path.join(caminho_pasta_imagens, nome_imagem)

    posicao = None

    # Inicio da contagem de timeout
    inicio = time.time()

    while posicao is None:
        posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
        if posicao is not None:
            logger.info("Imagem encontrada:", nome_imagem)
        else:
            if posicao:
                pyautogui.moveTo(posicao)
                return posicao

            if time.time() - inicio > timeout:
                monitor.registrar_erro(
                    "aguarda_imagem",
                    f"Timeout imagem {nome_imagem}"
                )

                logger.error(f"Timeout de {timeout} segundos atingido. Imagem {nome_imagem} não encontrada.")
                return None

            time.sleep(1)    

def abrir_vscode():
    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('vs_code', caminho_pasta_imagens), confidence=0.7))
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(posicoes.tela_vs_code)
    pyautogui.click()

def login_sap():
    try:
        # Abre o SAP
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite('sap')
        time.sleep(1)
        pyautogui.press('enter')
        aguarda_imagem('sap_aberto.png')

    except Exception as e:

        monitor.registrar_excecao(
            "login_sap",
            str(e)
        )

        logger.erro(f'Erro ao fazer o login ({e})')
        sys.exit()

    try:
        # Entra na conexão utilizada
        pyautogui.press('down')
        pyautogui.press('enter')

    except Exception as e:
        monitor.registrar_excecao(
            "conexao_sap",
            str(e)
        )

        logger.error(f'Erro ao fazer conexão no SAP ({e})')
        sys.exit()

    try:
        # Faz o login
        aguarda_imagem('tela_login_sap.png')
        pyautogui.typewrite(posicoes.usuario)
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.typewrite(posicoes.senha)
        time.sleep(0.5)
        pyautogui.press('enter')
        aguarda_imagem('procura_transacao.png')

    except Exception as e:
        monitor.registrar_excecao(
            "login_sap",
            str(e)
        )

        logger.error(f'Erro ao fazer login no SAP ({e})')
        sys.exit()

def voltar_ao_sap():
    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('logo_sap', caminho_pasta_imagens), confidence=0.9))
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('sap_minimizado', caminho_pasta_imagens), confidence=0.9))
    #pyautogui.moveTo(posicoes.tela_aberta_sap)
    time.sleep(1)
    pyautogui.click()

# Função para definir se a extração será de forma imediata ou programada
def executa_momento_extracao(momento:int):
    try:
        if momento == 1:
            pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('botao_imediatamente', caminho_pasta_imagens), confidence=0.7))
            pyautogui.click()
    
        elif momento == 2:
            pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('botao_data_hora', caminho_pasta_imagens), confidence=0.7))
            pyautogui.click()
            time.sleep(1)
            pyautogui.typewrite(amanha.strftime("%d.%m.%Y"))
            pyautogui.press('tab')
            pyautogui.typewrite('02:00')
    
        else:
            logger.error('Digite um valor válido! (1 ou 2)')

    except Exception as e:
        logger.error(f'Erro ao executar o momento para extração ({e})')

# Função usada para retornar os pedidos do FUP de acordo com a tabela passada como argumento 
def retorna_pedidos(caminho: str, aba_planilha:str):
    if aba_planilha == 'base migo_miro':
        
        df = pd.read_excel(caminho, 'base migo_miro')

        df = df.loc[14:]

        df.columns = df.loc[14]

        df.drop(axis=0, index=14, inplace=True)

        df = df['Doc.compra']

        df.drop_duplicates(inplace=True)

        return df.to_list()
    
    elif aba_planilha == 'app':
        
        df = pd.read_excel(caminho, 'APP')
        
        df.columns = df.loc[0]

        df.drop(axis=0, index= 0, inplace=True)

        df = df['PEDIDO']

        df.drop_duplicates(inplace=True)

        return df.to_list()

    else:
        monitor.registrar_erro(
            "retorna_pedidos",
            "Aba inválida"
        )

        logger.error('Favor informar uma das opções a seguir:\n1) base migo_miro\n2) app\n')

# Função para copiar e colar os pedidos no SAP
def copia_cola_pedidos(aba_planilha:str):

    try:
        # Atualizando um arquivo .txt com os números dos pedidos atuais
        with open("a pedidos.txt", 'w') as f:
            for pedido in retorna_pedidos(caminho_fup_atual, aba_planilha):
                f.write(f"{pedido}\n")

        abrir_vscode()
        
        aguarda_imagem('pedidos_txt.png')

        # Abrindo o arquivo                                                                                                                                     
        pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('pedidos_txt', caminho_pasta_imagens), confidence=0.7))
        pyautogui.doubleClick()

        time.sleep(0.7)

        # Copiando os valores
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')

        time.sleep(1)

        aguarda_imagem('arquivo_py.png')

        # volta para a tela do scrip
        pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('arquivo_py', caminho_pasta_imagens), confidence=0.7))
        pyautogui.doubleClick()

        # Volta ao SAP
        voltar_ao_sap()

        aguarda_imagem('selecao_multipla_sap.png')

        # Colando os valores no SAP
        pyautogui.hotkey('shift', 'f12')
        time.sleep(1)
        pyautogui.press('f8')

        time.sleep(1.5)
    except Exception as e:
        monitor.registrar_excecao(
            "copia_cola_pedidos",
            str(e)
        )

        raise

def copia_cola_estoque(arquivo:str):
            abrir_vscode()

            pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho(arquivo, caminho_pasta_imagens), confidence= 0.7))
            pyautogui.doubleClick()

            time.sleep(0.7)

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')

            voltar_ao_sap()

            time.sleep(1.5)

            pyautogui.press('up')
            pyautogui.moveTo(posicoes.clipboard_sap)
            pyautogui.click()
            time.sleep(0.7)
            pyautogui.press('f8')

            time.sleep(2)  

# Função para salvar a extração em excel de forma automatizada
def automacao_salvar_excel(momento:int, **kwargs):
    nome_arquivo = ''

    # Looping para definir o nome do arquivo de acordo com o tipo de extração
    if momento == 3:
        nome_arquivo = 'Pedidos de Compras'        
    elif momento == 4:
        for chave, valor in kwargs.items():
            nome_arquivo = f'Protocolos {valor}'
    elif momento == 5:
        nome_arquivo = 'Agendamentos'     
    else:

        monitor.registrar_erro(
            "automacao_salvar_excel",
            "Momento inválido"
        )
        logger.error('Escolha uma extração válida para essa função')

    pyautogui.press('backspace')
    pyautogui.typewrite(f'{nome_arquivo} {hoje.strftime("%d.%m.%Y")}')

    for i in range(7):
        pyautogui.press('tab')
    pyautogui.press('enter')
    
    time.sleep(1)

    caminho = r'C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\automacao FUP\Bases'

    pyperclip.copy(caminho)
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.press('enter')

    time.sleep(2)

    for i in range(9):
        pyautogui.press('tab')
    pyautogui.press('enter')

    aguarda_imagem('sap_salvar.png')

    # Permissão para salvar
    for i in range(4):
        pyautogui.press('tab')

    pyautogui.press('enter')

    aguarda_imagem('sap_salvar.png')

    for i in range(4):
        pyautogui.press('tab')
    pyautogui.press('enter')

    aguarda_imagem('arquivo_excel.png')

    # Mudando o arquivo para XLSX no Excel
    time.sleep(2)
    pyautogui.moveTo(posicoes.arquivo)
    pyautogui.click()
    time.sleep(1.7)
    for i in range(6):
        pyautogui.press('down')    
    time.sleep(1)
    for i in range(4):
        pyautogui.press('tab')
    pyautogui.typewrite(f'{nome_arquivo} {hoje.strftime("%d.%m.%Y")}')
    pyautogui.press('down')
    pyautogui.press('enter')
    for i in range(6):
        pyautogui.press('up')
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.hotkey('alt', 'f4')

# Função para fechar a transação e o programa SAP
def fechar_sap():
    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('logo_sap_aberto', caminho_pasta_imagens), confidence=0.7))
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(posicoes.tela_aberta_sap)
    pyautogui.click()
    time.sleep(1)
    
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('enter')

    time.sleep(2)

    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('logo_sap_aberto', caminho_pasta_imagens), confidence=0.7))
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(posicoes.tela_aberta_sap) #tela_aberta_sap = pyautogui.Point(x=1411, y=873) 
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')

# Função que retorna ao menu de opções
def voltar_ao_menu():
    opcao_final = int(input('Deseja voltar ao menu de seleção de automações?\n[1] Sim\n[2] Não\n'))

    if opcao_final == 1:
        fechar_sap()
              
    else:
        monitor.cancelar_execucao()
        logger.error('Finalizando as extrações por hoje!')
        sys.exit()

# Função para entrar na transação de protocolos
def entra_transacao_protocolos():

    # Faz o login no sistema SAP
    login_sap()

    # Entra na transação de protocolos
    pyautogui.typewrite(posicoes.transacao_extracao_protocolos)
    pyautogui.press('enter')

    aguarda_imagem('zt3000.png')

    for i in range(30):
        pyautogui.press('tab')
    pyautogui.press('right')

    time.sleep(1)

    for i in range(2):
        pyautogui.press('tab')
    pyautogui.press('right')

    time.sleep(1)

    # Move até a transação protocolos_compras_nf 
    pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('protocolos_compras_nf', caminho_pasta_imagens), confidence=0.7))
    pyautogui.doubleClick()

    aguarda_imagem('transacao_protocolos.png')

# Função que executa a extração de protocolos
def execucao_protocolos(empresa:str):
    try:
        pyautogui.typewrite(empresa)
        pyautogui.press('enter')
        #pyautogui.moveTo(posicoes.tipo_nf)
        time.sleep(0.5)
        #pyautogui.click()
        pyautogui.typewrite('*')

        time.sleep(0.5)

        pyautogui.moveTo(posicoes.selecao_multipla_protocolo)
        pyautogui.doubleClick()

        # Copia e cola os pedidos da tabela base migo miro
        copia_cola_pedidos('base migo_miro')

        pyautogui.press('f8')

        aguarda_imagem('protocolos.png')

        pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('protocolos', caminho_pasta_imagens), confidence=0.7))
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.press('down')
        pyautogui.press('enter')

        aguarda_imagem('exportar_como.png')

        pyautogui.typewrite(f'Protocolos {empresa}')
        time.sleep(1)

        pyautogui.press('enter')

        aguarda_imagem('salvar_como_excel.png')

        for i in range(7):
            pyautogui.press('tab')
            time.sleep(1)

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        caminho = r'C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\automacao FUP\Bases'

        time.sleep(1)

        pyperclip.copy(caminho)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.hotkey('alt', 'l')

        aguarda_imagem('sap_salvar.png')
        time.sleep(1)
        pyautogui.hotkey('alt', 'p')

        aguarda_imagem('sap_salvar.png')

        pyautogui.hotkey('alt', 'p')

        aguarda_imagem('arquivo_excel.png')
        pyautogui.hotkey('alt', 'f4')

        time.sleep(1)
        
        fechar_sap()
    except Exception as e:

        monitor.registrar_excecao(
            "execucao_protocolos",
            str(e)
        )

        raise
