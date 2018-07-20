"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa Emerenciano     8921421

Módulo responsável pelos métodos de pré-processamento do conjunto de dados
"""



# Módulos necessários
from arvore import get_classe_majoritaria, get_raiz_do_conjunto, monta_arvore
from manipulacaoArquivos import write_arvore_no_arquivo
from preProcessamento import trata_conjunto
from sklearn.utils import shuffle




def quebrar_conjunto(arquivo_entrada):
    """
    Quebra o conjunto presente no @arquivo_entrada em conjunto de treinamento, validação e testes
    """

    # Limpa e discretiza
    conjunto = trata_conjunto(
        arquivo_entrada=arquivo_entrada,
        char_a_remover='?',
        numero_de_grupos=3
    )
    conjunto = shuffle(conjunto)

    # Quebra o conjunto de dados
    quebrar_em = 3
    tamanho_particao = len(conjunto) / quebrar_em
    lista_de_conjuntos = [quebrar_em]

    i = 0
    while(i < quebrar_em):
        inicio = int((i * tamanho_particao))
        fim = int(((tamanho_particao * (i + 1)) - 1))

        lista_de_conjuntos.insert(i, conjunto.iloc[inicio : fim])

        i = i + 1

    return lista_de_conjuntos[0], lista_de_conjuntos[1], lista_de_conjuntos[2]



def treina(arquivo_entrada, arvore_gerada):
    """
    Treina o conjunto de dados presente @arquivo_entrada.
    Salva o modelo na @arvore_gerada
    """
    conjunto = trata_conjunto(
        arquivo_entrada=arquivo_entrada,
        char_a_remover='?',
        numero_de_grupos=3
    )

    raiz = get_raiz_do_conjunto(
        conjunto=conjunto
    )
    classe_majoritaria = get_classe_majoritaria(
        conjunto=conjunto
    )
    monta_arvore(
        conjunto_completo=conjunto,
        conjunto_atual=conjunto,
        conjunto_teste=conjunto,
        raiz=raiz,
        nome_da_raiz=raiz.name,
        classe_majoritaria=classe_majoritaria,
        arquivo_saida_testes='',
        arquivo_saida_treinamento='',
        deve_testar_enquanto_monta=False
    )

    write_arvore_no_arquivo(
        arvore=raiz,
        arquivo=arvore_gerada
    )

    return raiz


