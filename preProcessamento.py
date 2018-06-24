"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa                 8921421

Módulo responsável pelos métodos de pré-processamento do conjunto de dados
"""



# Módulos necessários
import pandas as pd
import Orange



def trata_conjunto(arquivo_entrada, char_a_remover='?', numero_de_grupos=3):
    """
    Lê o @arquivo_entrada, efetua sua limpeza e discretiza
    """

    arquivo_limpo = arquivo_entrada.replace('.csv', '_limpo.csv')
    arquivo_discr = arquivo_entrada.replace('.csv', '_discr.csv')

    remove_missing_values(
        arquivo_entrada=arquivo_entrada,
        arquivo_saida=arquivo_limpo,
        char=char_a_remover,
        encoding='utf-8'
    )

    discretiza(
        arquivo_entrada=arquivo_limpo,
        arquivo_saida=arquivo_discr,
        numero_de_grupos=numero_de_grupos
    )

    return pd.read_csv(arquivo_discr)



def remove_missing_values(arquivo_entrada, arquivo_saida, char='?', encoding='utf-8'):
    # pylint: disable=W0612
    """
    Método que remove os missing values do conjunto de entrada.

    Dado o @arquivo_entrada, lê e remove todas as linhas que possuem o @char
    Salvando no @arquivo_saida com a codificação @encoding
    """

    linhas_a_remover = []
    conjunto = pd.read_csv(arquivo_entrada)

    for indice, linha in conjunto.iterrows():
        for coluna in conjunto:
            conjunto[coluna].at[indice] = str(conjunto[coluna].at[indice]).strip()

            if(conjunto[coluna].iloc[indice] == char):
                linhas_a_remover.append(indice)
    
    # Apaga as linhas e recalcula os índices
    conjunto = conjunto.drop(linhas_a_remover)
    conjunto = conjunto.reset_index(drop=True)

    # Escreve no arquivo de saída
    conjunto.to_csv(arquivo_saida, encoding=encoding)
    return conjunto



def limpa_arquivo_discretizado(arquivo_entrada, arquivo_saida, encoding='utf-8'):
    """
    Limpa o conjunto de dados discretizado

    Usando o Orange para discretizar acabamos com alguns lixos e caracteres espesciais no conjunto.
    Lê o @arquivo_entrada, limpa e salva no @arquivo_saida usando o @encoding
    """

    dados = pd.read_csv(arquivo_entrada)
    dados = dados.drop([0, 1])
    dados = dados.drop(columns=['Feature 1'])
    dados = dados.reset_index(drop=True)
    dados.to_csv(arquivo_entrada, encoding=encoding, index=False)

    # Remove caracteres especiais
    arquivo_como_texto = ''
    with open(arquivo_entrada) as obj_file:
        arquivo_como_texto = arquivo_como_texto + obj_file.read() + '\n'

    arquivo_como_texto = arquivo_como_texto.replace('≥', '>=').replace(' - ', '-').replace('&amp;', '&')

    # Salva o arquivo
    with open(arquivo_saida, 'w') as obj_file:
        obj_file.write(arquivo_como_texto)



def discretiza(arquivo_entrada, arquivo_saida, numero_de_grupos):
    """
    Método de discretização

    Usa a biblioteca Orange para discretizar os dados usando entropia.
    Lê o @arquivo_entrada, aplica a discretização e salva no @arquivo_saida
    """

    conjunto = Orange.data.Table(arquivo_entrada)

    discretizacao_obj = Orange.preprocess.Discretize()
    discretizacao_obj.method = Orange.preprocess.discretize.EqualFreq(n=numero_de_grupos)
    
    conjunto_discretizado = discretizacao_obj(conjunto)
    Orange.data.Table.save(conjunto_discretizado, arquivo_saida)

    limpa_arquivo_discretizado(
        arquivo_entrada=arquivo_saida,
        arquivo_saida=arquivo_saida
    )


