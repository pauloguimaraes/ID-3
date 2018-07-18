"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Execução da pós-poda em uma árvore gerada
"""



# Módulos necessários
from arvore import get_classe_majoritaria, get_raiz_da_arvore, get_raiz_do_conjunto, monta_arvore
from datetime import datetime
from treinaModelo import quebrar_conjunto
from imprime import imprime_arvore, processa_impressao

import sys, getopt



def main(argv):
   # pylint: disable=W0612
    """
    Função de execução
    """
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])

    except getopt.GetoptError:
        print('usingTreinaModelo.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingTreinaModelo.py -i <inputfile> -o <outputfile>')
            sys.exit()

        elif(opt in ('-i', '--ifile')):
            inputfile = arg
        
        elif(opt in ('-o', '--ofile')):
            outputfile = arg
    # # Quebra o conjunto em TREINAMENTO, VALIDAÇÃO e TESTES
    # # Salva em arquivos na pasta designada
    # print('Início da divisão do conjunto: {0}'.format(datetime.now()))

    treinamento, validacao, teste = quebrar_conjunto(
        arquivo_entrada=inputfile
    )

    # print('Fim da divisão do conjunto: {0}'.format(datetime.now()))


    # # Monta a árvore
    # print('Início da montagem da árvore: {0}'.format(datetime.now()))

    raiz = get_raiz_do_conjunto(
        conjunto=treinamento
    )
    major_class = get_classe_majoritaria(
        conjunto=treinamento
    )
    
    monta_arvore(
        conjunto_completo=treinamento,
        conjunto_atual=treinamento,
        conjunto_teste=teste,
        raiz=raiz,
        nome_da_raiz=raiz.name,
        classe_majoritaria=major_class,
        arquivo_saida_treinamento='',
        arquivo_saida_testes='',
        deve_testar_enquanto_monta=False
    )

    raiz = get_raiz_da_arvore(no=raiz)
    
    dicionario = dict()
    imprime_arvore(raiz, dicionario, validacao)
    print(processa_impressao(dicionario))
    # print('Fim da poda: {0}'.format(datetime.now()))



if(__name__ == '__main__'):
    main(sys.argv[1:])
