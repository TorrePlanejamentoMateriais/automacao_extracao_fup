" ======================================================================="
" ====================== REGISTRO DE MANUTENÇÃO ========================="
" ======================================================================="



"""
=============================================================
Projeto         : Automação SAP
Módulo          : SAP
Arquivo         : sap.py

Criado por      : GUSTAVO ALMEIDA HERMOGENES
Data Criação    : -------

Última Alteração
-------------------------------------------------------------
User            : Z701038
Dev             : Tiago Eneas Antunes
Data            : 31/08/2026
Hora            : 17:21

Descrição       : FLuxo princiap da automação FUP.
=============================================================
"""



" ======================================================================="
" ====================== BIBLIOTECAS PRINCIAPAIS ========================="
" ======================================================================="


import pandas as pd
import pyautogui
import time
from datetime import datetime
import sys
import os
import pyperclip

" ======================================================================="
" ========================= FUNÇÕES AUXILIARES =========================="
" ======================================================================="


from utils.limpeza_dados import df_para_excel
from utils.posicoes import Posicoes
from utils.obter_usuario import obter_usuario
from config.caminhos import caminho_monitoramento_automacao
from utils.uteis import *

from classes.monitor import MonitorExecucao

" ======================================================================="
" ====================== CAMINHOS E VARIÁVEIS ==========================="
" ======================================================================="


# Diretório do FUP que será usado em algumas extrações
caminho_pasta_fup = r"C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\Planilhas FUP\data"

# Diretório onde as imagens estão armazenadas
caminho_pasta_imagens = r"C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\Imagens_automacao_fup"

# Diretório onde os protocolos extraídos foram salvos
caminho_pasta_protocolos = r"C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\automacao FUP\Bases"

# Diretório onde o protocolo concatenado será salvo
caminho_final = r"C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\automacao FUP\Resultado"

# Garante que não vai lançar exceção de imagem não encontrada
pyautogui.useImageNotFoundException(False)

# Cálculo de datas que serão usadas durante a execução do programa
hoje = datetime.datetime.today()
amanha = hoje + datetime.timedelta(days=1)
data_anterior = hoje - datetime.timedelta(days=30)


" ======================================================================="
" ========================= FUNÇÃO PRINCIPAL ============================"
" ======================================================================="


def main():

    monitor = MonitorExecucao()
    posicao = Posicoes()

    logger.info('Iniciando Automação FUP .........................................................')

    try:
        while True:

            opcao = menu()

            if opcao == 1:

                # Define se a extração será imediata ou em background
                try:

                    momento_extracao = int(input("Selecione a opção de extração desejada:\n[1] Imediatamente\n[2] Programado\n"))
                except Exception as e:

                    monitor.registrar_execao(
                        'tipo_extracao',
                        str(e)
                    )

                    logger.error(f'Erro ao verificar o modeo de extração: \n{e}')
                    print(f'Erro ao verificar o modo de extração:\n{e}')
                    

                # Faz o login no sistema SAP
                login_sap()

                # Entra na transação
                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('procura_transacao', caminho_pasta_imagens)))
                pyautogui.typewrite(posicoes.transacao_extracao_fup)
                pyautogui.press('enter')

                aguarda_imagem('transacao_fup.png')

                for i in range(11):
                    pyautogui.press('tab')
                pyautogui.press('enter')

                # Copia e cola os pedidos da base migo_miro
                copia_cola_pedidos('base migo_miro')

                # Fazendo os filtros
                # Apagando a sinalização 'x'
                for i in range(26):
                    pyautogui.press('tab')
                pyautogui.press('backspace')

                for i in range(56):
                    pyautogui.press('tab')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite('/PLAN.MAT')

                time.sleep(0.5)

                # Executando 
                pyautogui.press('f9')
                aguarda_imagem('avancar_background.png')
                pyautogui.hotkey('shift', 'f1')
                aguarda_imagem('imediatamente_ou_programado.png')

                # Define se será imediatamente ou programado
                executa_momento_extracao(momento_extracao)  
                
                time.sleep(0.5)

                pyautogui.press('enter')
                pyautogui.hotkey('ctrl', 's')

                voltar_ao_menu()

            elif opcao == 2:

                # Define se a extração será imediata ou em background
                try:
                    momento_extracao = int(input("Selecione a opção de extração desejada:\n[1] Imediatamente\n[2] Programado\n"))
                except Exception as e:

                    monitor.registrar_execao(
                        'tipo_extracao',
                        str(e)
                    )

                    logger.error(f'Erro ao verificar o modo de extração:\n{e}')
                    print(f'Erro ao verificar o modo de extração:\n{e}')
                    

                # Faz o login no sistema SAP
                login_sap()

                # Entra na transação
                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('procura_transacao', caminho_pasta_imagens)))
                pyautogui.typewrite(posicoes.transacao_extracao_fup)
                pyautogui.press('enter')

                aguarda_imagem('transacao_fup.png')

                for i in range(18):
                    pyautogui.press('tab')
                # Data inicial
                pyautogui.typewrite(str(data_anterior.strftime("%d.%m.%Y")))
                pyautogui.press('tab')

                # Data de hoje
                pyautogui.typewrite(str(hoje.strftime("%d.%m.%Y")))

                for i in range(7):
                    pyautogui.press('tab')
                pyautogui.press('enter')

                aguarda_imagem('criado_por.png')

                # Colocando os usuários que criaram pedidos
                pyautogui.typewrite('Z577883')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('z094118')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')    
                pyautogui.typewrite('Z126207')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')    
                pyautogui.typewrite('92051209')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')    
                pyautogui.typewrite('Z229770')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('F162499')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('Z255065')
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('92050730')
                pyautogui.press('enter')
                time.sleep(1.0)
                pyautogui.press('pgdn')
                time.sleep(1.0)
                pyautogui.press('enter')
                time.sleep(1.0)
                pyautogui.press('down')
                pyautogui.typewrite('N5771226')     
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('f8')

                time.sleep(0.7)

                # Fazendo os filtros
                # Apagando a sinalização 'x'
                for i in range(11):
                    pyautogui.press('tab')
                pyautogui.press('backspace')

                for i in range(56):
                    pyautogui.press('tab')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite('/PLAN.MAT')

                time.sleep(0.5)

                # Executando 
                pyautogui.press('f9')
                aguarda_imagem('avancar_background.png')
                pyautogui.hotkey('shift', 'f1')
                aguarda_imagem('imediatamente_ou_programado.png')

                # Define se será imediatamente ou programado
                executa_momento_extracao(momento_extracao)  
                
                time.sleep(0.5)

                pyautogui.press('enter')
                pyautogui.hotkey('ctrl', 's')

                voltar_ao_menu()

            elif opcao == 3:

                # Faz o login no sistema SAP
                login_sap()

                # Entra na transação
                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('procura_transacao', caminho_pasta_imagens)))
                pyautogui.typewrite(posicoes.transacao_extracao_compras)
                pyautogui.press('enter')

                aguarda_imagem('transacao_compras.png')

                # Fazendo os filtros
                for i in range(15):
                    pyautogui.press('tab')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite('ALV')

                time.sleep(0.5)

                # Seleções dinâmicas
                pyautogui.hotkey('shift', 'f4')
                time.sleep(1)
                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('requisicao', caminho_pasta_imagens), confidence=0.7))
                pyautogui.click() 
                pyautogui.press('right')       
                time.sleep(1)

                for i in range(13):
                    pyautogui.press('down')
                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('compras_criado_por', caminho_pasta_imagens), confidence=0.7))
                pyautogui.doubleClick()
                time.sleep(1.5)

                pyautogui.moveTo(pyautogui.locateOnScreen(retorna_caminho('requisicao', caminho_pasta_imagens), confidence=0.7))
                pyautogui.click()

                for i in range(2):
                    pyautogui.press('tab')
                pyautogui.press('enter')

                aguarda_imagem('criado_por.png')

                # Pedidos criados por Douglas, Ramon e William
                pyautogui.typewrite('Z577883')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('z094118')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('Z229770')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('Z255065')
                time.sleep(0.5)
                pyautogui.press('down')
                pyautogui.typewrite('F162499')
                time.sleep(0.5)
                pyautogui.press('f8')

                time.sleep(1)

                for i in range(55):
                    pyautogui.press('tab')
                pyautogui.press('space')

                pyautogui.press('tab')
                pyautogui.press('tab')

                pyautogui.press('space')

                # Executar
                pyautogui.press('f8')

                aguarda_imagem('pedidos_compras.png', timeout=150)

                # Transformando em excel
                pyautogui.hotkey('ctrl', 'shift', 'f9')
                aguarda_imagem('salvar_em_excel.png', timeout=150)

                pyautogui.press('down')
                pyautogui.press('enter')

                aguarda_imagem('aguarda_salvar_excel.png', timeout=150)

                for i in range(6):
                    pyautogui.press('tab')
                
                caminho = r'C:\Users\F252727\Documents\Projetos Py v1\GUSTAVO\automacao FUP\Bases'

                pyperclip.copy(caminho)
                pyautogui.hotkey('ctrl', 'v')

                pyautogui.press('tab')
                pyautogui.typewrite('Pedidos de Compras.XLS')
                pyautogui.press('enter')

                aguarda_imagem('sap_salvar.png')

                for i in range(4):
                    pyautogui.press('tab')
                pyautogui.press('enter')

                time.sleep(1)

                voltar_ao_menu()

            elif opcao == 4:
                
                # Empresa 001
                entra_transacao_protocolos()
                execucao_protocolos('001')
                time.sleep(2)


                #fechar_sap()

                # Empresa 881
                entra_transacao_protocolos()
                execucao_protocolos('881')
                time.sleep(2)
                #fechar_sap()

                # Empresa 705
                entra_transacao_protocolos()
                execucao_protocolos('705')
                time.sleep(2)

    #            excel = pyautogui.locateOnScreen(retorna_caminho('excel', caminho_pasta_imagens), confidence=0.7)
    #            if excel:
    #                pyautogui.click()
    #                time.sleep(1)
    #                pyautogui.press('right')
    #                pyautogui.press('enter')
    #                for i in range(4):
    #                    pyautogui.moveTo(posicoes.fechar_excel)
    #                    pyautogui.click()
    #                    time.sleep(2)
    #            time.sleep(2)

                protocolos_001 = retorna_caminho('Protocolos 001', caminho_pasta_protocolos)
                protocolos_705 = retorna_caminho('Protocolos 705', caminho_pasta_protocolos)
                protocolos_881 = retorna_caminho('Protocolos 881', caminho_pasta_protocolos)

                df1 = pd.read_excel(protocolos_001)
                df2 = pd.read_excel(protocolos_705)
                df3 = pd.read_excel(protocolos_881)

                df_concatenado = pd.concat([df1, df2, df3])

                df_para_excel(df_concatenado, caminho_final, 'Protocolos')

                voltar_ao_menu()

            elif opcao == 5:
                
                # Faz login no sistema SAP
                login_sap()

                # Entra na transação de protocolos
                pyautogui.typewrite(posicoes.transacao_extracao_protocolos)
                pyautogui.press('enter')

                aguarda_imagem('zt3000.png')

                img1 = pyautogui.locateOnScreen(retorna_caminho('monitor', caminho_pasta_imagens), confidence=0.7)
                print(img1)
                time.sleep(1)
                pyautogui.doubleClick(img1)

                aguarda_imagem('agendamentos.png')
                img2 = pyautogui.locateOnScreen(retorna_caminho('agendamentos', caminho_pasta_imagens), confidence=0.7)
                time.sleep(0.5)
                pyautogui.doubleClick(img2)            

                # Insere os pedidos do APP 
                for i in range(6):
                    pyautogui.press('tab')

                pyautogui.press('enter')
                time.sleep(1.5)
                copia_cola_pedidos('app')

                # Roda os agendamentos
                time.sleep(1.5)
                pyautogui.press('f8')

                for i in range(43):
                    pyautogui.press('tab')

                time.sleep(1)
                pyautogui.press('enter')

                # Vai no símbolo de exportar para excel
                aguarda_imagem('protocolos.png')
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                pyautogui.press('down')
                pyautogui.press('enter')
                aguarda_imagem('selecionar_planilha_eletronica.png')
                pyautogui.press('enter')

                aguarda_imagem('salvar_como.png')

                # Salva o arquivo em excel
                automacao_salvar_excel(5)

                voltar_ao_menu()
            
            elif opcao == 6:
                # Define se a extração será imediata ou em background
                try:
                    logger.info('Selecionado a opção de extração')
                    momento_extracao = int(input("Selecione a opção de extração desejada:\n[1] Imediatamente\n[2] Programado\n"))
                    logger.info(f'Tipo de Extração selecionado: {momento_extração}')

                except Exception as e:

                    monitor.registrar_execao(
                        'tipo_extracao',
                        str(e)
                    )


                    print(f'Erro ao verificar o modo de extração:\n{e}')
                    logger.error(f'Erro ao verificar o modo de extração:\n{e}')
                    
            
                # faz login no SAP
                login_sap()

                # Transação MB52
                pyautogui.typewrite('mb52')
                pyautogui.press('enter')
                aguarda_imagem('mb52.png')

                # Centros
                for i in range(5):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                time.sleep(0.7)

                copia_cola_estoque('centros_empresarial.png')

                # Depósitos
                for i in range(4):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                time.sleep(1)

                copia_cola_estoque('depositos_empresarial.png') 

                # Layout
                for i in range(23):
                    pyautogui.press('tab')
                pyautogui.typewrite('/EVANDRO')

                # Execução da extração
                pyautogui.moveTo(posicoes.programa)
                pyautogui.click()
                time.sleep(1)
                for i in range(3):
                    pyautogui.press('down')
                pyautogui.press('enter')
                time.sleep(0.7)
                pyautogui.hotkey('shift', 'f1')
                time.sleep(0.5)
                executa_momento_extracao(momento_extracao)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 's')

                voltar_ao_menu()

            elif opcao == 7:
                # Define se a extração será imediata ou em background
                try:
                    momento_extracao = int(input("Selecione a opção de extração desejada:\n[1] Imediatamente\n[2] Programado\n"))
                except Exception as e:
                    
                    monitor.registrar_execao(
                        'tipo_extracao',
                        str(e)
                    )

                    print(f'Erro ao verificar o modo de extração:\n{e}')

                    logger.error(f'Erro ao verificar o modo de extração:\n{e}')
                    

                # Faz Login no SAP
                login_sap()
                
                # Transação MB52
                pyautogui.typewrite('mb52')
                pyautogui.press('enter')
                aguarda_imagem('mb52.png')

                # Remove os códigos de material que não são necessários
                for i in range(2):
                    pyautogui.press('tab')
                pyautogui.press('enter')

                time.sleep(0.7)

                pyautogui.moveTo(posicoes.excluir_intervalos)
                pyautogui.click()
                time.sleep(0.7)
                pyautogui.typewrite('41001552')
                pyautogui.press('down')
                pyautogui.typewrite('41001376')
                pyautogui.press('down')
                pyautogui.typewrite('41001573')
                pyautogui.press('f8')

                time.sleep(0.7)

                # Centros
                for i in range(4):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                time.sleep(0.7)

                copia_cola_estoque('centros_residencial.png')

                # Depósitos
                for i in range(4):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.moveTo(posicoes.excluir_intervalos)
                pyautogui.click()
                time.sleep(0.7)

                copia_cola_estoque('depositos_residencial.png') 

                # Tipo de Material
                for i in range(7):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.moveTo(posicoes.excluir_intervalos)
                pyautogui.click()
                time.sleep(0.7)
                pyautogui.typewrite('ZPBL')
                pyautogui.press('down')
                pyautogui.typewrite('MISC')
                pyautogui.press('f8')
                time.sleep(0.7)

                # Layout
                for i in range(17):
                    pyautogui.press('tab')
                pyautogui.typewrite('/EVANDRO')

                # Execução da extração
                pyautogui.moveTo(posicoes.programa)
                pyautogui.click()
                time.sleep(1)
                for i in range(3):
                    pyautogui.press('down')
                pyautogui.press('enter')
                time.sleep(0.7)
                pyautogui.hotkey('shift', 'f1')
                time.sleep(0.5)
                executa_momento_extracao(momento_extracao)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 's')

                voltar_ao_menu()

            else:

                monitor.registrar_erro(
                    'menu',
                    'valor_não_existente_no_menu'
                ) 

                print('\nPor favor, digite um número válido')
                logger.error('\nPor favor, digite um número válido')
                time.sleep(3)
                continue

    except Exception as e:

        monitor.registrar_excecao(
            "main_opção_inválida",
            str(e)
        )

        print(f'Erro! Favor selecionar uma opção válida.\n{e}')
        logger.error(f'Erro! Favor selecionar uma opção válida.\n{e}')
        

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        monitor.cancelar_execucao()

        print(
            "Execução interrompida pelo usuário"
        )

        logger.info(
            "Execução interrompida pelo usuário"
        )

    except Exception as e:

        monitor.registrar_excecao(
            "main",
            str(e)
        )

        print(e)
        logger.error(e)

    finally:

        monitor.finalizar(
            usuario=obter_usuario(),
            caminho_monitoramento=caminho_monitoramento_automacao,
            nome_automacao="FUP"
        )



