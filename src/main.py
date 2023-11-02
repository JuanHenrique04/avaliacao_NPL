import pandas as pd
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from string import punctuation

vetorizar = CountVectorizer(max_features=25)

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

##################################################################################################

def separa_frases(conteudo_resumo):
    frases = conteudo_resumo.split('.')
    print(frases)

##################################################################################################
#remove stopwors com pontos

def remove_stopwords(resumo_tokens):

    palavras_irrelevantes = nltk.corpus.stopwords.words("portuguese") #cria uma lista de stopwords
    #abaixo é acrescentado pontuação a lista de stopwords
    pontuacao = list()
    for ponto in punctuation:
        pontuacao.append(ponto)
    total_stopwords = pontuacao + palavras_irrelevantes

    #abaixo é retirada as stopwords dos tokens e reune o resumo
    frase_processada = list()
    nova_frase = list()
    for palavra in resumo_tokens:
        if palavra not in total_stopwords:
            nova_frase.append(palavra)
    frase_processada.append(' '.join(nova_frase))

    texto_processado = frase_processada
    print(texto_processado, '\n')
    return texto_processado

##################################################################################################
#separa novamente em tokens SEM as stopwords

def tokenizacao_sem_stopwords(resumo_processado):
    tokens_sem_stopwords = nltk.word_tokenize(resumo_processado[0])
    print(tokens_sem_stopwords)
    frequencia = nltk.FreqDist(tokens_sem_stopwords)
    df_frequencia = pd.DataFrame({"Palavra": list(frequencia.keys()),
                                  "Frequencia": list(frequencia.values())})
    df_frequencia = df_frequencia.nlargest(columns="Frequencia", n= 25)
    print(df_frequencia)
    return df_frequencia

##################################################################################################

def monta_grafo(dados_df):
    G = nx.Graph()

    for palavra in dados_df['Palavra'].values:
        palavra = G.add_node(palavra)
        vertices = list(G.nodes)

    G.add_edge(vertices[0], vertices[1])

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            G.add_edge(vertices[i], vertices[j])
            
    plt.figure(figsize=(12,8))
    nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True)
    plt.show()
    return G

##################################################################################################

#separa as palavras mais frequentes
# def palavras_mais_frequentes(texto):
#     bag_of_words = vetorizar.fit_transform(texto)
#     print(vetorizar.get_feature_names_out(), '\n')
#     matriz_esparsa = pd.DataFrame.sparse.from_spmatrix(bag_of_words, columns=vetorizar.get_feature_names_out())
#     print(matriz_esparsa, '\n')
#     return matriz_esparsa

##################################################################################################


input_arquivo = input("Nome do arquivo: ")
nome_arquivo = f"./resumos/{input_arquivo}"

artigo = read_file(nome_arquivo)
resumo = artigo[1].lower()
# separa_frases(resumo)
tokens = nltk.word_tokenize(resumo) #separa todas as palavras do resumo

valores_df = tokenizacao_sem_stopwords(remove_stopwords(tokens))
# print(valores_df['Palavra'].values)
# print(valores_df['Frequencia'].values)

monta_grafo(valores_df)
remove_stopwords(tokens)