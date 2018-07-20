"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa Emerenciano     8921421

Módulo para cálculo de entropia e ganho para atributos
"""



# Módulos necessários
import math



def entropia(conjunto, rotulo):
    """
    Calcula a entropia do conjunto, usando o rotulo para base do cálculo
    """

    # Conjunto de valores possíveis para cada @rotulo
    conjunto_de_rotulos = set(conjunto[rotulo])
    qtd_exemplos_por_valor = dict()

    # Conta o número de exemplos para cada um dos valores possíveis
    for valor in conjunto_de_rotulos:
        qtd_exemplos_por_valor[valor] = len(conjunto[(conjunto[rotulo] == valor)]
        )

    # Ordena a lista de forma a usar o elemento com mais ocorrências primeiro no cálculo
    entropias_ordenadas = sorted(
        qtd_exemplos_por_valor.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Calcula a entropia
    entropia_do_conjunto = 0
    for item in entropias_ordenadas:
        valor = int(item[1])

        # 0 * log(0) = 0
        if(valor == 0):
            entropia_do_conjunto = entropia_do_conjunto - 0
        else:
            p = valor / len(conjunto)
            entropia_do_conjunto = entropia_do_conjunto - (p * (math.log(p) / math.log(2)))
    
    return entropia_do_conjunto



def ganho(conjunto, atributo, rotulo):
    """
    Calcula o ganho do @atributo no conjunto, usando o rotulo como classificação
    """

    # Tamanho do conjunto de dados
    tamanho_do_conjunto = len(conjunto)

    # Cria um subconjunto para cada um dos valores possíveis para o @atributo
    conjunto_de_rotulos = set(conjunto[atributo])
    qtd_exemplos_por_valor = dict()
    subconjunto = dict()

    # Também conta o número de ocorrências para cada valor
    for valor in conjunto_de_rotulos:
        subconjunto[valor] = conjunto[(conjunto[atributo] == valor)]
        qtd_exemplos_por_valor[valor] = len(subconjunto[valor])

    # Ordena as ocorrências de forma a a recuperar a maior primeiro
    ganhos_ordenados = sorted(
        qtd_exemplos_por_valor.items(),
        key=lambda x: x[1],
        reverse=True
    )
    # print(ganhos_ordenados)

    # Calcula o ganho
    ganho_para_atributo = 0
    for item in ganhos_ordenados:
        entropia_do_subconjunto = entropia(
            conjunto=subconjunto[str(item[0])],
            rotulo=rotulo
        )
        p = int(item[1]) / tamanho_do_conjunto
        ganho_para_atributo = ganho_para_atributo - (p * entropia_do_subconjunto)
    
    ganho_para_atributo = entropia(conjunto=conjunto, rotulo=atributo) + ganho_para_atributo
    # print('{0} é o ganho para {1}'.format(ganho_para_atributo, atributo))
    return ganho_para_atributo


