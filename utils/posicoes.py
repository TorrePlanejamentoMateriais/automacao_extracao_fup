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

Descrição       : Arquivo onde fica as posições de cada botão na tela.
=============================================================
"""

" ======================================================================="
" ====================== BIBLIOTECAS PRINCIPAIS ========================="
" ======================================================================="


# %% 
import pyautogui
import time


# %%

" ======================================================================="
" ============================= LOGIN ==================================="
" ======================================================================="
class Posicoes:
    abre_sap = pyautogui.Point(x=574, y=1057)
    conexao_sap = pyautogui.Point(x=339, y=224)
    usuario = 'f252727'
    senha = 'Chimbica@09'
    procura_transacao = pyautogui.Point(x=217, y=91)

    " ======================================================================="
    " ============================= COORDENADAS =============================="
    " ======================================================================="

    #python -m mouseinfo

    # FUP
    transacao_extracao_fup = 'Y_D01_16000084'
    excluir_x = pyautogui.Point(x=488, y=653)
    campo_documento_compras = pyautogui.Point(x=1053, y=383)
    vs_code = pyautogui.Point(x=1036, y=1059)
    tela_vs_code = pyautogui.Point(x=1055, y=903)
    pedidos_txt= pyautogui.Point(x=124, y=437)
    copia_pedidos= pyautogui.Point(x=75, y=184)
    #tela_aberta_sap = pyautogui.Point(x=617, y=889)
    tela_aberta_sap = pyautogui.Point(x=1411, y=873)            
    tela_transacaoo = pyautogui.Point(x=86, y=66)
    clipboard_sap = pyautogui.Point(x=1217, y=759)
    seta_avancar_sap = pyautogui.Point(x=736, y=768)
    campo_data = pyautogui.Point(x=529, y=477)
    campo_layout = pyautogui.Point(x=538, y=892)
    programa = pyautogui.Point(x=102, y=44)
    background = pyautogui.Point(x=138, y=147)
    avancar_background = pyautogui.Point(x=757, y=592)
    botao_imediatamente = pyautogui.Point(x=109, y=353)
    botao_verificar = pyautogui.Point(x=651, y=940)
    botao_gravar = pyautogui.Point(x=755, y=937)
    data_hora = pyautogui.Point(x=301, y=351)

    # -------------------------------------------------------

    # Pedido de Compras
    transacao_extracao_compras = 'me5a'
    abrangencia_lista = pyautogui.Point(x=492, y=418)
    caixa_requisicao1 = pyautogui.Point(x=35, y=554)
    caixa_requisicao2 = pyautogui.Point(x=42, y=608)
    selecoes_dinamicas = pyautogui.Point(x=117, y=214)
    seta_requisicao_compra = pyautogui.Point(x=42, y=308)
    criado_por = pyautogui.Point(x=117, y=485)
    selecao_multipla = pyautogui.Point(x=1368, y=329)
    botao_transferir = pyautogui.Point(x=902, y=767)
    botao_executar = pyautogui.Point(x=44, y=211)
    lista = pyautogui.Point(x=82, y=40)
    avancar_excel = pyautogui.Point(x=656, y=707)
    este_computador = pyautogui.Point(x=145, y=717)
    windows = pyautogui.Point(x=341, y=426)
    usuarios = pyautogui.Point(x=307, y=564)
    meu_usuario = pyautogui.Point(x=328, y=475)
    nome_arquivo = pyautogui.Point(x=498, y=889)
    salvar_arquivo = pyautogui.Point(x=976, y=898)
    gustavo = pyautogui.Point(x=387, y=475)
    python = pyautogui.Point(x=336, y=507)
    automacao = pyautogui.Point(x=313, y=389)
    resultado = pyautogui.Point(x=343, y=452)
    arquivo = pyautogui.Point(x=60, y=104)
    salvar_como = pyautogui.Point(x=90, y=521)
    mudar_nome = pyautogui.Point(x=975, y=228)

    # Protocolos
    transacao_extracao_protocolos = 'zt3000'
    relatorios = pyautogui.Point(x=66, y=897)
    protocolos = pyautogui.Point(x=80, y=864)
    protocolos_compras_nf = pyautogui.Point(x=120, y=830)
    #tipo_nf = pyautogui.Point(x=511, y=598)
    tipo_nf = pyautogui.Point(x=511, y=494)
    #selecao_multipla_protocolo = pyautogui.Point(x=1063, y=418)
    selecao_multipla_protocolo = pyautogui.Point(x=828, y=329)
    executar_protocolos = pyautogui.Point(x=47, y=213)
    exportar_protocolos = pyautogui.Point(x=296, y=263)
    fechar_excel = pyautogui.Point(x=1890, y=37)
    fechar_transacao_sap = pyautogui.Point(x=1833, y=20)
    fechar_sap = pyautogui.Point(x=668, y=191)
    monitor = pyautogui.Point(x=127, y=712)
    selecao_multipla_agendamento = pyautogui.Point(x=1455, y=469)
    selecionar = pyautogui.Point(x=1543, y=862)
    exportar_excel = pyautogui.Point(x=979, y=452)

    excluir_intervalos = pyautogui.Point(x=617, y=350)