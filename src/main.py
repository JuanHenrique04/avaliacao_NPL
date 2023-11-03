import pandas as pd
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from string import punctuation

vetorizar = CountVectorizer()

#ler o arquivo
def read_file(arquivo):
    try:
        with open(arquivo, "r") as arq:
            conteuto = arq.readlines()
            return conteuto
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def separa_frases(conteudo_resumo):
    frases = conteudo_resumo.split('.')
    frases.pop(-1)
    return frases

#remove stopwors com pontos
def remove_stopwords(resumo_str):
    tokens = nltk.word_tokenize(resumo_str) #separa todas as palavras do resumo

    palavras_irrelevantes = nltk.corpus.stopwords.words("portuguese") #cria uma lista de stopwords
    #abaixo é acrescentado pontuação a lista de stopwords
    pontuacao = list()
    for ponto in punctuation:
        pontuacao.append(ponto)
    total_stopwords = pontuacao + palavras_irrelevantes

    #abaixo é retirada as stopwords dos tokens e reune o resumo
    frase_processada = list()
    nova_frase = list()
    for palavra in tokens:
        if palavra not in total_stopwords:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase))

    texto_processado = frase_processada
    return texto_processado

#separa novamente em tokens SEM as stopwords
def monta_df(resumo_processado):
    tokens_sem_stopwords = nltk.word_tokenize(resumo_processado[0])
    print(tokens_sem_stopwords)
    frequencia = nltk.FreqDist(tokens_sem_stopwords)
    df_frequencia = pd.DataFrame({"Palavra": list(frequencia.keys()),
                                  "Frequencia": list(frequencia.values())})
    df_frequencia = df_frequencia.nlargest(columns="Frequencia", n= 25)
    print(df_frequencia)
    return df_frequencia

def monta_grafo(dados_df):
    G = nx.Graph()

    for palavra in dados_df['Palavra'].values:
        palavra = G.add_node(palavra)
        vertices = list(G.nodes)

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            G.add_edge(vertices[i], vertices[j])
            
    plt.figure(figsize=(12,8))
    nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True)
    plt.show()
    return G

def monta_grafo_por_frase(frases):
    G = nx.Graph()
    
    for frase_tokenizada in frases:
        for palavra in frase_tokenizada:
            palavra = G.add_node(palavra)
            vertices = list(G.nodes)

    for frase_tokenizada in frases:
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                G.add_edge(vertices[i], vertices[j])
                
    plt.figure(figsize=(12,8))
    nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True,)
    plt.show()
    return G

# input_arquivo = input("Nome do arquivo: ")
nome_arquivo = f"./resumos/{'arq_1.txt'}"

artigo = read_file(nome_arquivo)
titulo = artigo[0]
resumo = artigo[1].lower()
tags = artigo[2]

frases = separa_frases(resumo)
# print(frases)

frases_sem_stopwords = []
for frase in frases:
    frases_sem_stopwords.append(remove_stopwords(frase))
    
print(frases_sem_stopwords)

frases_tokenizadas = []
for frase_process in frases_sem_stopwords:
    frases_tokenizadas.append(nltk.word_tokenize(frase_process[0]))

monta_df(remove_stopwords(resumo))
monta_grafo_por_frase(frases_tokenizadas)

# texto_sem_stopwords = remove_stopwords(resumo)
# valores_df = monta_df(texto_sem_stopwords)

# print(valores_df['Palavra'].values)
# print(valores_df['Frequencia'].values)

# monta_grafo(valores_df)
# remove_stopwords(resumo)