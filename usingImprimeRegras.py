"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Execução do treinamento de um modelo e impressão de suas regras (IF-THEN)
"""



# Módulos necessários
from arvore import get_classe_majoritaria, get_raiz_da_arvore, get_raiz_do_conjunto, monta_arvore
from datetime import datetime
from imprime import get_dicionario_de_regras, processa_impressao
from manipulacaoArquivos import write_regras
from treinaModelo import quebrar_conjunto

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
        print('usingImprimeRegras.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingImprimeRegras.py -i <inputfile> -o <outputfile>')
            print('O parâmetro <inputfile> DEVE ser um arquivo CSV. O parâmetro <outputfile> DEVE ser um arquivo TXT.\n')
            print('Exemplo: \n')
            print('usingImprimeRegras.py -i \'./imprime-regras/conjuntos/adult.csv\' -o \'./imprime-regras/saidas/regras.txt\'')
            sys.exit()

        elif(opt in ('-i', '--ifile')):
            inputfile = arg
        
        elif(opt in ('-o', '--ofile')):
            outputfile = arg


    # Quebra o conjunto em TREINAMENTO, VALIDAÇÃO e TESTES
    print('Início da divisão do conjunto: {0}'.format(datetime.now()))

    treinamento, validacao, teste = quebrar_conjunto(
        arquivo_entrada=inputfile
    )

    print('Fim da divisão do conjunto: {0}'.format(datetime.now()))

    # Monta a árvore
    print('Início da montagem da árvore: {0}'.format(datetime.now()))

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

    print('Fim da montagem da árvore: {0}'.format(datetime.now()))

    # Imprime as regras
    print('Início da impressão das regras: {0}'.format(datetime.now()))

    raiz = get_raiz_da_arvore(no=raiz)
    
    dicionario = dict()
    get_dicionario_de_regras(raiz, dicionario, validacao)

    s = processa_impressao(dicionario)
    write_regras(outputfile, s)

    print('Fim da impressão das regras: {0}'.format(datetime.now()))



if(__name__ == '__main__'):
    main(sys.argv[1:])
