import os
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode

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

def processar_resumo(summary):
    frases = dividir_frases(summary)

    palavras = []
    for frase in frases:
        palavras_divididas = dividir_palavras(frase)
        # Remove as stop words e converte para minúsculas atraves da biblioteca unidecode
        palavras.extend([unidecode(token.lower()) for token in palavras_divididas if token.lower() not in stop_words])
    return palavras


# Itera sobre a lista de arquivos
for arquivo in arquivos:
    caminho_arquivo = os.path.join(diretorio, arquivo)
    
    with open(caminho_arquivo, 'r') as file:

        linhas = file.readlines()
        titulo = linhas[0] 
        resumo = linhas[1]
        palavras_chaves = linhas[2]

        resumo_processado = processar_resumo(resumo)

    print("Resumo processado: ", arquivo)
    print(resumo_processado)
    print('\n')