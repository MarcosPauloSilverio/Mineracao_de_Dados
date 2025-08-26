# Importando as bibliotecas necessárias para a manipulação dos dados
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

pd.set_option('display.encoding', 'utf-8')

# 1. Carregar o arquivo CSV
try:
    df = pd.read_csv('clientes_supervida.csv', on_bad_lines='skip')
    print("Arquivo 'clientes_supervida.csv' carregado com sucesso!")
except FileNotFoundError:
    print("Erro: O arquivo 'clientes_supervida.csv' não foi encontrado.")
    print("Certifique-se de que o arquivo CSV e o script Python estão na mesma pasta.")
    exit()

# 2. Reorganizar e renomear as colunas
df = df.rename(columns={
    'id_cliente': 'id_cliente',
    'nome_cliente': 'nome_cliente',
    'sobrenome_cliente': 'sobrenome_cliente',
    'data_nascimento': 'data_nascimento',
    'sexo': 'sexo',
    'email_cliente': 'email_cliente',
    'aceita_receber_newsletter': 'aceita_receber_newsletter',
    'celular_cliente': 'celular_cliente',
    'whatsapp': 'whatsapp',
    'aceita_receber_mensagens': 'aceita_receber_mensagens',
    'fixo_cliente': 'fixo_cliente',
    'Street Name': 'logradouro',
    'Street Number': 'numero',
    'bairro': 'bairro',
    'cep': 'cep',
    'estado': 'estado'
})
print("Colunas renomeadas e padronizadas.")

# 3. Gerar datas de nascimento realistas (caso as originais estejam no futuro)
hoje = datetime.now()
data_min = hoje - timedelta(days=65*365) # Idade máxima: 65 anos
data_max = hoje - timedelta(days=18*365) # Idade mínima: 18 anos
delta = data_max - data_min
num_clientes = len(df)
df['data_nascimento'] = [data_min + timedelta(days=np.random.randint(delta.days)) for _ in range(num_clientes)]
print("Datas de nascimento realistas geradas.")

# 4. Tratamento de valores nulos e e-mails
df['email_cliente'] = df['email_cliente'].fillna('')
provedores = ['gmail.com', 'hotmail.com']
df['email_cliente'] = df['email_cliente'].apply(
    lambda x: f"{x.split('@')[0]}@{np.random.choice(provedores)}" if pd.notnull(x) and '@' in x else f"cliente_{np.random.randint(1000, 9999)}@{np.random.choice(provedores)}"
)
print("E-mails ajustados para Gmail e Hotmail.")

# 5. Traduzir a coluna 'sexo' e ajustar as booleanas
df['sexo'] = df['sexo'].replace({'Male': 'Masculino', 'Female': 'Feminino'})
df['sexo'] = df['sexo'].apply(lambda x: 'Outros' if x not in ['Masculino', 'Feminino'] else x)
df['aceita_receber_newsletter'] = df['aceita_receber_newsletter'].replace({True: 'Sim', False: 'Não'})
df['whatsapp'] = df['whatsapp'].replace({True: 'Sim', False: 'Não'})
df['aceita_receber_mensagens'] = df['aceita_receber_mensagens'].replace({True: 'Sim', False: 'Não'})
print("Coluna de gênero e booleanas traduzidas e ajustadas.")

# 6. Gerar bairros e CEPs para o cenário do Rio de Janeiro (CORRIGIDO)
bairros_rj = ['Copacabana', 'Tijuca', 'Barra da Tijuca']
ceps_rj = {
    'Copacabana': [f'220{i:03d}-000' for i in range(1, 10)],
    'Tijuca': [f'205{i:03d}-000' for i in range(1, 10)],
    'Barra da Tijuca': [f'226{i:03d}-000' for i in range(1, 10)]
}
df['bairro'] = np.random.choice(bairros_rj, num_clientes)
df['cep'] = df['bairro'].apply(lambda x: np.random.choice(ceps_rj[x]))
df['estado'] = 'RJ'
print("Bairros, CEPs e Estado ajustados para o cenário do Rio de Janeiro.")

# 7. Adicionar dados de compra fictícios
df['ticket_medio'] = np.random.uniform(50, 500, num_clientes).round(2)
df['produtos_saudaveis_percentual'] = np.random.uniform(0, 100, num_clientes).round(2)
print("Dados de ticket médio e percentual de produtos saudáveis adicionados.")

# 8. Salvando o arquivo CSV com todas as alterações
df.to_csv('clientes_supervida_ajustado_final.csv', index=False)
print(f"Novo arquivo 'clientes_supervida_ajustado_final.csv' foi salvo com as alterações.")

