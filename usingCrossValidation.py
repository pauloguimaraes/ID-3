"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Execução do Cross-Validation para um determinado conjunto de dados
"""



# Módulos necessários
from crossValidation import cross_validation

import sys, getopt



def main(argv):
    # pylint: disable=W0612
    """
    Função de execução
    """

    inputfile = ''
    pastaconjuntos = ''
    pastaarvores = ''

    try:
        opts, args = getopt.getopt(
            argv,
            'hi:d:t:',
            ['ifile=', 'dpath=', 'tpath=']
        )
    
    except getopt.GetoptError:
        print('usingCrossValidation.py -i <inputfile> -d <datasetspath> -t <treespath>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingCrossValidation.py -i <inputfile> -d <datasetspath> -t <treespath>\n')
            print('Os parâmetros <datasetspath> e <treespath> DEVEM terminar com / \n')
            print('Exemplo: \n')
            print('python3 ./usingCrossValidation.py -i \'./files/cross-validation/datasets/adult.csv\' -d \'./files/cross-validation/datasets/\' -t \'./files/cross-validation/trees/\'')
            sys.exit()

        elif(opt in ('-i', '--ifile')):
            inputfile = arg

        elif(opt in ('-d', '--dpath')):
            pastaconjuntos = arg

        elif(opt in ('-t', '--tpath')):
            pastaarvores = arg
        

    # Executa o 10-fold cross-validation
    cross_validation(
        arquivo_entrada=inputfile,
        numero_de_folds=10,
        deve_gerar_arquivos=True,
        pasta_conjuntos=pastaconjuntos,
        pasta_arvores=pastaarvores
    )




if __name__ == '__main__':
    main(sys.argv[1:])