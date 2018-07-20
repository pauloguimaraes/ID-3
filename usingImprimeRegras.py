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
from treinaModelo import quebrar_conjunto
from imprime import get_dicionario_de_regras, processa_impressao
from manipulacaoArquivos import write_regras

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

    treinamento, validacao, teste = quebrar_conjunto(
        arquivo_entrada=inputfile
    )

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
    get_dicionario_de_regras(raiz, dicionario, validacao)

    s = processa_impressao(dicionario)
    write_regras(outputfile, s)



if(__name__ == '__main__'):
    main(sys.argv[1:])
