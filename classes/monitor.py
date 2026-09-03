from datetime import datetime
import pandas as pd
import os


class MonitorExecucao:

    def __init__(self):

        self.inicio = datetime.now()

        self.qtd_erros = 0
        self.qtd_excecoes = 0

        self.status = "SUCESSO"

        self.funcoes_com_erro = []

        self.meses = {
            1: "JAN",
            2: "FEV",
            3: "MAR",
            4: "ABR",
            5: "MAI",
            6: "JUN",
            7: "JUL",
            8: "AGO",
            9: "SET",
            10: "OUT",
            11: "NOV",
            12: "DEZ"
        }

    def registrar_erro(self, funcao, erro=""):
        """
        Erro controlado.
        Exemplo:
        - Timeout
        - Imagem não encontrada
        - Arquivo não encontrado
        """

        self.qtd_erros += 1

        self.funcoes_com_erro.append(
            f"{funcao}: {erro}"
        )

    def registrar_excecao(self, funcao, erro=""):
        """
        Exceções capturadas em blocos try/except.
        """

        self.qtd_excecoes += 1
        self.qtd_erros += 1

        self.status = "ERRO"

        self.funcoes_com_erro.append(
            f"{funcao}: {erro}"
        )
        
    def cancelar_execucao(self):
        self.status = "CANCELADO"

    def finalizar(
        self,
        usuario,
        caminho_monitoramento,
        nome_automacao="FUP"
    ):

        fim = datetime.now()

        tempo_execucao = round(
            (fim - self.inicio).total_seconds(),
            2
        )

        # ============================
        # Histórico acumulado
        # ============================

        if os.path.exists(caminho_monitoramento):

            df_existente = pd.read_excel(
                caminho_monitoramento
            )

            total_execucoes = len(df_existente) + 1

            total_erros = (
                df_existente[
                    "QtdErroDuranteExec"
                ].sum()
                + self.qtd_erros
            )

            if "Status" in df_existente.columns:

                total_sucessos = len(
                    df_existente[
                        df_existente["Status"]
                        == "SUCESSO"
                    ]
                )

                total_falhas = len(
                    df_existente[
                        df_existente["Status"]
                        == "ERRO"
                    ]
                )

            else:

                total_sucessos = 0
                total_falhas = 0

        else:

            total_execucoes = 1
            total_erros = self.qtd_erros

            total_sucessos = 0
            total_falhas = 0

        # Somando a execução atual

        if self.status == "SUCESSO":
            total_sucessos += 1
        else:
            total_falhas += 1

        # ============================
        # Registro atual
        # ============================

        dados = {
            "NumeroExecucao": [total_execucoes],
            "User": [usuario],
            "DataAtual": [
                fim.strftime("%d/%m/%Y")
            ],
            "InicioExec": [
                self.inicio.strftime("%H:%M:%S")
            ],
            "FimExec": [
                fim.strftime("%H:%M:%S")
            ],
            "TempoTotalExec": [
                tempo_execucao
            ],
            "NomeAutomacao": [
                nome_automacao
            ],
            "Mes": [
                self.meses[fim.month]
            ],
            "Ano": [
                fim.year
            ],

            # Situação da execução
            "Status": [
                self.status
            ],

            # Execução atual
            "QtdErroDuranteExec": [
                self.qtd_erros
            ],

            "QtdExcecoes": [
                self.qtd_excecoes
            ],

            # Totais históricos
            "TotalExecucoes": [
                total_execucoes
            ],

            "TotalErros": [
                total_erros
            ],

            "TotalSucessos": [
                total_sucessos
            ],

            "TotalFalhas": [
                total_falhas
            ],

            "FuncoesComErro": [
                " | ".join(
                    self.funcoes_com_erro
                )
            ]
        }

        novo_registro = pd.DataFrame(dados)

        # ============================
        # Salvar Excel
        # ============================

        if os.path.exists(caminho_monitoramento):

            df_existente = pd.read_excel(
                caminho_monitoramento
            )

            df_final = pd.concat(
                [
                    df_existente,
                    novo_registro
                ],
                ignore_index=True
            )

        else:

            df_final = novo_registro

        df_final.to_excel(
            caminho_monitoramento,
            index=False
        )