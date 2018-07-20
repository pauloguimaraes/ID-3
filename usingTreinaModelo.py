"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Treina o modelo presente no arquivo passado como parâmetro
Usado, principalmente, para o PlayTennis
"""



# Módulos necessários
from treinaModelo import treina
import pandas as pd

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
            print('O parâmetro <inputfile> DEVE ser um arquivo CSV. O parâmetro <outputfile> NÃO deve ter extensão.\n')
            print('Exemplo: \n')
            print('usingTreinaModelo.py -i \'./play_tennis/conjuntos/play_tennis.csv\' -o \'./play_tennis/arvores/gerada\'')
            sys.exit()

        elif(opt in ('-i', '--ifile')):
            inputfile = arg
        
        elif(opt in ('-o', '--ofile')):
            outputfile = arg

    # Treina a árvore, salvando no arquivo de saída
    conjunto = pd.read_csv(inputfile)
    raiz = treina(
        arquivo_entrada=inputfile,
        arvore_gerada=outputfile+'.json'
    )



if(__name__ == '__main__'):
    main(sys.argv[1:])