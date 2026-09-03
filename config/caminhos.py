" ======================================================================="
" ====================== REGISTRO DE MANUTENÇÃO ========================="
" ======================================================================="


"""
=============================================================
Projeto         : Automação SAP
Arquivo         : logger.py

Criado por      : Tiago Eneas Antunes
Data Criação    : 01/09/2026

Última Alteração
-------------------------------------------------------------
User            : Z701038
Dev             : Tiago Eneas Antunes
Data            : 01/09/2026
Hora            : 11:52

Descrição       : Configuração centralizada de caminhos de planilhas e imagens.
=============================================================
"""

" ======================================================================="
" ====================== BIBLIOTECAS PRINCIPAIS ========================="
" ======================================================================="

import os


" ======================================================================="
" ====================== FUNÇÕES AUXILIARES ============================="
" ======================================================================="
from utils.obter_usuario import obter_usuario



# Caminho da planilha que irá monitar a automação FUP
user = obter_usuario()
caminho_monitoramento_automacao = rf'C:\Users\{user}\Desktop\Monitoramento Automações\Dados\automacoes\fup\log.xlsx'
