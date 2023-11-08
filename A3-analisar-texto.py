import os
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('portuguese'))

# Diretório dos arquivos e armazenamento dos arquivos em lista
diretorio = './a3-analise-textual/BaseDadosResumos'
arquivos = os.listdir(diretorio)

#Função para dividir o resumo em frases
def dividir_frases(resumo):
    frases = resumo.split('.')
    return frases

#Função para dividir as frases em palavras
def dividir_palavras(frase):
    palavras = frase.split()
    return palavras

def processar_resumo(resumo):
    frases = dividir_frases(resumo)

    palavras = []
    for frase in frases:
        palavras_divididas = dividir_palavras(frase)

        # Remove as stop words e converte e faz a conversão para letras minúsculas atraves da biblioteca unidecode
        # ***** retirar biblioteca unidecode e criar função para deixar as letras minusculas manualmente *****
        palavras.extend([unidecode(token.lower()) for token in palavras_divididas if token.lower() not in stop_words])
    print(palavras)
    return palavras

topicos = {}
nome_arquivo = input("Digite o nome do arquivo: ")

if nome_arquivo in arquivos:
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_arquivo, 'r') as file:
        linhas = file.readlines()
        titulo = linhas[0] 
        resumo = linhas[1]
        palavras_chaves = linhas[2]

        resumo_processado = processar_resumo(resumo)

        # Identifica tópicos usando NMF
        vetorizar = TfidfVectorizer()
        identificar_topicos = vetorizar.fit_transform([' '.join(resumo_processado)])
        modelo_nmf = NMF(n_components = 5)
        modelo_nmf.fit(identificar_topicos)

        # Mapear tópicos e palavras-chave 
        #topicos[nome_arquivo] = [f'Tópico {i}' for i in range(len(modelo_nmf.components_))]

    # Construção do grafo de tópicos da biblioteca networkx
    G = nx.Graph()

    #Adiciona nós e arestas ao grafo com base na coocorrência das palavras
    for i, primeira_palavra in enumerate(resumo_processado):
        for c, segunda_palavra in enumerate(resumo_processado):
            if i != c:
                if G.has_edge(primeira_palavra, segunda_palavra):
                    G[primeira_palavra][segunda_palavra]['weight'] += 1
                else:
                    G.add_edge(primeira_palavra, segunda_palavra, weight=1)

    # Calcula o PageRank para cada palavra
    scores = nx.pagerank(G)

    # Exibe as palavras mais importantes com base no PageRank
    palavras_principais = sorted(scores, key=scores.get, reverse=True)[:5]
    print("Arquivo processado: ", nome_arquivo)
    print(resumo_processado)
    print("Palavras Principais:", palavras_principais)
    print('\n')

    # Cria um novo grafo apenas com as palavras principais e suas conexões
    G_palavras_principais = G.subgraph(palavras_principais)

    # Visualiza o grafo das palavras principais
    pos = nx.spring_layout(G_palavras_principais)
    labels = nx.get_edge_attributes(G_palavras_principais, 'weight')
    nx.draw(G_palavras_principais, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G_palavras_principais, pos, edge_labels=labels)
    plt.show()
else:
    print("O arquivo especificado não está na lista de arquivos.")




