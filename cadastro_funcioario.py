import pandas as pd
from datetime import datetime

# Verifica se o arquivo já existe
def carrega_dados_existentes(arquivo):
    try:
        return pd.read_excel(arquivo)
    except FileNotFoundError:
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não existir

# Nome do arquivo Excel
arquivo_excel = 'cadastro_usuario.xlsx'

# Carrega dados existentes (se houver)
dados_existentes = carrega_dados_existentes(arquivo_excel)

while True:
    dados = dict()
    dados['Nome'] = str(input('Nome: '))
    nasc = int(input('Ano de Nascimento: '))
    dados['Idade'] = datetime.now().year - nasc
    dados['Nº CTPS'] = str(input('Carteira de Trabalho (0 se não tiver): '))  # Mudei para str
    
    if dados['Nº CTPS'] == '0':
        dados['Nº CTPS'] = 'não possui ctps'  # Preenche com 'não possui ctps'
        dados['Contratação'] = None
        dados['Salário'] = None
        dados['Aposentadoria'] = None
    else:
        dados['Contratação'] = int(input('Ano de Contratação: '))
        dados['Salário'] = round(float(input('Salário: R$').replace(',', '.')), 2)

        # Calcular anos até a aposentadoria
        dados['Aposentadoria'] = dados['Idade'] + ((dados['Contratação'] + 35) - datetime.now().year)

    # Criar um DataFrame com os dados e remover colunas vazias
    novo_dados = pd.DataFrame([dados]).dropna(axis=1, how='all')

    # Adicionar os dados do usuário ao DataFrame existente
    dados_existentes = pd.concat([dados_existentes, novo_dados], ignore_index=True)
    
    continuar = str(input('Deseja continuar cadastrando usuários [S/N]: '))[0].strip().upper()
    if continuar != 'S':
        break

# Salvar todos os dados (novos e existentes) em uma planilha Excel
dados_existentes.to_excel(arquivo_excel, index=False)

print("As informações foram salvas com sucesso em '{}'".format(arquivo_excel))
