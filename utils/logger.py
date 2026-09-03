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
Hora            : 08:56

Descrição       : Configuração centralizada de logs.
=============================================================
"""

" ======================================================================="
" ====================== BIBLIOTECAS PRINCIPAIS ========================="
" ======================================================================="


import logging
import os
from datetime import datetime

" ======================================================================="
" ====================== FUNÇÕES AUXILIARES ============================="
" ======================================================================="
from utils.obter_usuario import obter_usuario


" ======================================================================="
" ========================= FUNÇÃO PRINCIPAL ============================"
" ======================================================================="


meses = {
    1:  "JAN",
    2: "FEV",
    3:  "MAR",
    4:  "ABR",
    5:  "MAI",
    6:  "JUN",
    7:  "JUL",
    8:  "AGO",
    9:  "SET",
    10: "OUT",
    11: "NOV",
    12 : "DEZ",
}

def cria_pasta_arquivo_diario():
    
    data_atual = datetime.today()

    data_formatada = data_atual.strftime("%d-%m-%y")

    mes_abrev = meses[data_atual.month]

    user = obter_usuario()

    caminho_pasta = (
        rf"C:\Users\{user}\Desktop\Refaturação Automação FUP"
        rf"\logs\{mes_abrev}\{data_formatada}"
    )

    os.makedirs(
        caminho_pasta,
        exist_ok=True
    )

def logger():

    cria_pasta_arquivo_diario()

    mes_atual = meses[datetime.today().month]

    data_atual = datetime.today()
    data_formatada = data_atual.strftime("%d-%m-%y")

    user = obter_usuario()

    caminho_arquivo = (
        rf"C:\Users\{user}\Desktop\Refaturação Automação FUP"
        rf"\logs\{mes_atual}\{data_formatada}\log_fup.txt"
    )

    logger = logging.getLogger("SAP_AUTOMACAO")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        caminho_arquivo,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger