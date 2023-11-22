import os
from matplotlib import pyplot as plt
import nltk
from unidecode import unidecode
import networkx as nx

nltk.download('punkt')

# Diretório dos arquivos e armazenamento dos arquivos em lista
diretorio = './a3-analise-textual/BaseDadosResumoAutores'
arquivos = os.listdir(diretorio)

#Essa função separa todos os nomes que estão depois de virgular e depois trata as palavras colocando em lowercase e acentuação
def tratar_palavras(autores):
    autores_virgula = autores.split(',')
    autores_limpos = [unidecode(token.lower()) for token in autores_virgula if token.lower()]
    return autores_limpos

lista_autores = []  # Lista para armazenar os autores de todos os arquivos

for arquivo in arquivos:
    caminho_arquivo = os.path.join(diretorio, arquivo)  # Caminho completo para o arquivo atual

    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        autores = linhas[3].strip()  # Remoção dos espaços em branco antes e depois dos nomes
        autores_tratados = tratar_palavras(autores)
        lista_autores.extend(autores_tratados)   

# Construção do grafo de tópicos da biblioteca networkx
grafo_autores = nx.Graph()

# Contagem de quantas vezes aparece cada autor
contagem_autores = {}
for autor in lista_autores:
    if autor in contagem_autores:
        contagem_autores[autor] += 1
    else:
        contagem_autores[autor] = 1

# Identificar os autores mais influentes
autores_mais_influentes = sorted(contagem_autores.items(), key=lambda x: x[1], reverse=True)[:10]
print(autores_mais_influentes)

#Adiciona nós e arestas ao grafo com base na quantidade de vezes que um autor aparece com outro em um mesmo arquivo
for i, primeira_autor in enumerate(autores_mais_influentes):
    for c, segunda_autor in enumerate(autores_mais_influentes):
        if i != c:
            if grafo_autores.has_edge(primeira_autor, segunda_autor):
                grafo_autores[primeira_autor][segunda_autor]['weight'] += 1
            else:
                grafo_autores.add_edge(primeira_autor, segunda_autor, weight=1)


# Cria um novo grafo apenas com os autores mais influentes e suas conexões
grafo_autores_influentes = grafo_autores.subgraph(autores_mais_influentes)

# Visualiza o grafo das dos autores mais influentes e quantas vezes um autor aparece com outro
pos = nx.spring_layout(grafo_autores_influentes)
labels = nx.get_edge_attributes(grafo_autores_influentes, 'weight')
nx.draw(grafo_autores_influentes, pos, with_labels=True)
nx.draw_networkx_edge_labels(grafo_autores_influentes, pos, edge_labels=labels)
plt.show()