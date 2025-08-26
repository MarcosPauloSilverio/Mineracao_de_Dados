# Importando as bibliotecas necessárias para a segmentação
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

pd.set_option('display.encoding', 'utf-8')

# 1. Carregar o arquivo de dados limpos
try:
    df = pd.read_csv('clientes_supervida_ajustado_final.csv')
    print("Arquivo 'clientes_supervida_ajustado_final.csv' carregado com sucesso!")
except FileNotFoundError:
    print("Erro: O arquivo 'clientes_supervida_ajustado_final.csv' não foi encontrado.")
    print("Certifique-se de que o arquivo está no mesmo diretório do script.")
    exit()

# 2. Selecionar as colunas para a segmentação
# Usaremos 'ticket_medio' e 'produtos_saudaveis_percentual' para encontrar o perfil ideal
X = df[['ticket_medio', 'produtos_saudaveis_percentual']]

# 3. Aplicar o algoritmo K-Means para criar os clusters
# Vamos definir 3 clusters para começar:
# 1. Clientes com baixo potencial
# 2. Clientes com potencial médio
# 3. Clientes de alto potencial (o nosso alvo)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

print("\nSegmentação de clientes concluída usando o algoritmo K-Means.")

# 4. Visualizar os clusters em um gráfico de dispersão
plt.figure(figsize=(12, 8))
sns.scatterplot(x='ticket_medio', y='produtos_saudaveis_percentual', data=df,
                hue='cluster', palette='viridis', style='cluster', s=100)
plt.title('Segmentação de Clientes por Padrão de Compra (Clusters K-Means)', fontsize=16)
plt.xlabel('Ticket Médio', fontsize=12)
plt.ylabel('Percentual de Produtos Saudáveis', fontsize=12)
plt.legend(title='Cluster')
plt.show()

# 5. Analisar o perfil de cada cluster
print("\n--- Análise dos Perfis de Cluster ---")
cluster_summary = df.groupby('cluster')[['ticket_medio', 'produtos_saudaveis_percentual']].agg(['mean', 'median', 'count'])
print(cluster_summary)

# Identificando o cluster de alto potencial
# O cluster com o maior ticket médio e maior percentual de saudáveis é o nosso alvo.
cluster_alvo = cluster_summary.loc[:, ('ticket_medio', 'mean')].idxmax()
print(f"\nO cluster de alto potencial para o programa de alimentação saudável é o: Cluster {cluster_alvo}")

# Exibindo os primeiros clientes do cluster alvo
print(f"\n--- Exemplo de Clientes do Cluster Alvo ({cluster_alvo}) ---")
print(df[df['cluster'] == cluster_alvo][['nome_cliente', 'sobrenome_cliente', 'bairro', 'ticket_medio', 'produtos_saudaveis_percentual']].head())

print("\nAnálise de segmentação concluída!")


