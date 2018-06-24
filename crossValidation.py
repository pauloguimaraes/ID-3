
"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa                 8921421

Módulo com métodos responsáveis por executar a validação K-Fold Cross-Validation
"""



# Módulos necessários
from arvore import get_acuracia, get_classe_majoritaria, get_erro, get_raiz_do_conjunto, monta_arvore
from manipulacaoArquivos import write_arvore_no_arquivo, write_conjunto_no_arquivo
from preProcessamento import trata_conjunto
from sklearn.utils import shuffle

import math



def cross_validation(arquivo_entrada, numero_de_folds=10, deve_gerar_arquivos=True, pasta_conjuntos='', pasta_arvores=''):
    """
    Executa o @numero_de_folds-Fold Cross-Validation para o conjunto presente no @arquivo_entrada

    Usa o parâmetro @deve_gerar_arquivos para decidir se teremos output, gerando os conjuntos na @pasta_conjuntos e as árvores na @pasta_arvores
    """

    erro_medio = 0

    # Faz a leitura do arquivo de entrada
    # Remove os missing values
    # Discretiza
    conjunto = trata_conjunto(
        arquivo_entrada=arquivo_entrada,
        char_a_remover='?',
        numero_de_grupos=3
    )

    # Mistura os dados
    conjunto = shuffle(conjunto)

    # Cria N partições e calcula o tamanho do fold
    lista_de_conjuntos = [numero_de_folds]
    tamanho_do_fold = len(conjunto) / numero_de_folds

    # Quebra o conjunto completo em N partições
    i = 0
    while(i < numero_de_folds):
        inicio = int((i * tamanho_do_fold))
        fim = int(((tamanho_do_fold * (i + 1)) - 1))

        lista_de_conjuntos.insert(i, conjunto.iloc[inicio : fim])

        i = i + 1

    # Executa N vezes, usando N-1 partições para treinamento e 1 partição para testes
    # Cada execução uma partição distinta será usada para testes
    x = 0
    erro = 0
    while(x < numero_de_folds):
        conjunto_treinamento = conjunto[0 : 0]
        conjunto_teste = conjunto[0 : 0]
        y = 0

        while(y < numero_de_folds):
            if(x == y):
                conjunto_teste = conjunto_teste.append(
                    lista_de_conjuntos[x],
                    ignore_index=True
                )
            else:
                conjunto_treinamento = conjunto_treinamento.append(
                    lista_de_conjuntos[x],
                    ignore_index=True
                )
            
            y = y + 1

        # Seleciona a raiz da árvore
        raiz = get_raiz_do_conjunto(
            conjunto=conjunto
        )
        # Recupera a classe majoritária
        major_class = get_classe_majoritaria(
            conjunto=conjunto_treinamento
        )

        print('Montando a {0}a árvore'.format(x+1))

        # Monta a árvore
        monta_arvore(
            conjunto_completo=conjunto_treinamento,
            conjunto_atual=conjunto_treinamento,
            conjunto_teste=conjunto_teste,
            raiz=raiz,
            nome_da_raiz=raiz.name,
            classe_majoritaria=major_class,
            arquivo_saida_treinamento='',
            arquivo_saida_testes='',
            deve_testar_enquanto_monta=False
        )

        # Recupera o erro dessa interação
        erro_deste_teste = get_erro(
            conjunto=conjunto_teste,
            arvore=raiz
        )
        erro = erro + erro_deste_teste

        print('Erro na {0}a interação: {1}'.format(x + 1, erro_deste_teste))

        x = x + 1

        if(deve_gerar_arquivos):
            # Escreve a árvore gerada nessa interação
            write_arvore_no_arquivo(
                arvore=raiz,
                arquivo=pasta_arvores+'modelo_{0}.json'.format(x)
            )

            # Escreve o conjunto de teste gerado nessa interação
            write_conjunto_no_arquivo(
                conjunto=conjunto_teste,
                arquivo=pasta_conjuntos+'teste_{0}.csv'.format(x)
            )

            # Escreve o conjunto de treinamento gerado nessa interação
            write_conjunto_no_arquivo(
                conjunto=conjunto_treinamento,
                arquivo=pasta_conjuntos+'treinamento_{0}.csv'.format(x)
            )
    

    # Calcula o erro médio e o erro verdadeiro
    erro_medio = erro / numero_de_folds
    print('Erro médio: {0}'.format(erro_medio))

    se = math.sqrt((erro_medio * (1 - erro_medio)) / len(conjunto))
    erro_verd_min = erro_medio - 1.96 * se
    erro_verd_max = erro_medio + 1.96 * se

    print('Com intervalo de confiança de 95% temos que o erro verdadeiro estará entre {0} por cento e {1} por cento'.format((erro_verd_min * 100), (erro_verd_max * 100)))

    return erro_medio


