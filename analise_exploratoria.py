# Importando as bibliotecas necessárias para a análise e visualização
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

pd.set_option('display.encoding', 'utf-8')

# Configurando o estilo dos gráficos para uma melhor visualização
sns.set_style('whitegrid')

# 1. Carregar o arquivo de dados limpos
try:
    df = pd.read_csv('clientes_supervida_ajustado_final.csv')
    print("Arquivo 'clientes_supervida_ajustado_final.csv' carregado com sucesso!")
except FileNotFoundError:
    print("Erro: O arquivo 'clientes_supervida_ajustado_final.csv' não foi encontrado.")
    print("Certifique-se de que o arquivo está no mesmo diretório do script.")
    exit()

# 2. Análise Demográfica: Distribuição de Clientes por Gênero e Bairro
print("\n--- Análise Demográfica ---")

# Gráfico de Barras: Distribuição de Clientes por Gênero
plt.figure(figsize=(8, 5))
sns.countplot(x='sexo', data=df, palette='viridis')
plt.title('Distribuição de Clientes por Gênero', fontsize=16)
plt.xlabel('Gênero', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.show()
print("Gráfico de distribuição por gênero gerado.")

# Gráfico de Barras: Distribuição de Clientes por Bairro
plt.figure(figsize=(10, 6))
sns.countplot(x='bairro', data=df, palette='plasma', order=df['bairro'].value_counts().index)
plt.title('Distribuição de Clientes por Bairro', fontsize=16)
plt.xlabel('Bairro', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.show()
print("Gráfico de distribuição por bairro gerado.")

# 3. Análise de Faixa Etária
# Para analisar a idade, primeiro vamos calcular a idade dos clientes
df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
hoje = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
df['idade'] = (hoje - df['data_nascimento']).dt.days // 365.25

# Definindo faixas etárias para agrupar os clientes
bins = [0, 12, 17, 24, 34, 44, 59, 100]
labels = ['Criança', 'Adolescente', 'Jovem Adulto', 'Adulto', 'Meia-Idade', 'Sênior', 'Idoso']
df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)

# Gráfico de Barras: Distribuição de Clientes por Faixa Etária
plt.figure(figsize=(12, 7))
sns.countplot(x='faixa_etaria', data=df, palette='rocket', order=labels)
plt.title('Distribuição de Clientes por Faixa Etária', fontsize=16)
plt.xlabel('Faixa Etária', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.xticks(rotation=45)
plt.show()
print("Gráfico de distribuição por faixa etária gerado.")

# 4. Exibindo as primeiras linhas do DataFrame com as novas colunas
print("\n--- Primeiras linhas do DataFrame com as novas colunas 'idade' e 'faixa_etaria' ---")
print(df[['nome_cliente', 'data_nascimento', 'idade', 'faixa_etaria', 'bairro', 'sexo']].head())

print("\nAnálise Exploratória de Dados (AED) concluída. Podemos prosseguir para a análise dos padrões de compra.")

# --- Análise de Padrões de Compra ---
print("\n--- Análise de Padrões de Compra ---")

# Gráfico de Dispersão: Ticket Médio vs. Produtos Saudáveis
plt.figure(figsize=(12, 8))
sns.scatterplot(x='ticket_medio', y='produtos_saudaveis_percentual', data=df,
                hue='faixa_etaria', style='sexo', palette='coolwarm', s=100, alpha=0.7)
plt.title('Relação entre Ticket Médio e Percentual de Produtos Saudáveis', fontsize=16)
plt.xlabel('Ticket Médio', fontsize=12)
plt.ylabel('Percentual de Produtos Saudáveis', fontsize=12)
plt.legend(title='Faixa Etária', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
print("Gráfico de dispersão gerado, mostrando a relação entre ticket médio e produtos saudáveis.")

# Identificando Clientes com Alto Potencial (alto ticket médio e alto percentual de saudáveis)
alto_potencial = df[(df['ticket_medio'] > df['ticket_medio'].median()) &
                    (df['produtos_saudaveis_percentual'] > df['produtos_saudaveis_percentual'].median())]

print("\n--- Clientes com Alto Potencial para o Programa ---")
print(f"Número de clientes com alto potencial: {len(alto_potencial)}")
print("\nTop 5 Clientes de Alto Potencial:")
print(alto_potencial[['nome_cliente', 'sobrenome_cliente', 'bairro', 'ticket_medio', 'produtos_saudaveis_percentual']].head())

print("\nAnálise de padrões de compra concluída. Próximo passo: Segmentação de Clientes.")

# 5. Traduzir a coluna 'sexo' e ajustar as booleanas (CORRIGIDO)
df['sexo'] = df['sexo'].replace({
    'Male': 'Masculino',
    'Female': 'Feminino'
})
# Agrupa quaisquer outros valores em 'Outros' para evitar erros
df['sexo'] = df['sexo'].apply(lambda x: 'Outros' if x not in ['Masculino', 'Feminino'] else x)

df['aceita_receber_newsletter'] = df['aceita_receber_newsletter'].replace({True: 'Sim', False: 'Não'})
df['whatsapp'] = df['whatsapp'].replace({True: 'Sim', False: 'Não'})
df['aceita_receber_mensagens'] = df['aceita_receber_mensagens'].replace({True: 'Sim', False: 'Não'})
print("Coluna de gênero e booleanas traduzidas e ajustadas.")

