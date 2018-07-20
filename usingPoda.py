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
from imprime import get_dicionario_de_regras, processa_impressao
from manipulacaoArquivos import write_arvore_no_arquivo, write_conjunto_no_arquivo, write_regras
from poda import efetua_poda
from treinaModelo import quebrar_conjunto

import sys, getopt



def main(argv):
    # pylint: disable=W0612
    """
    Função de execução
    """

    inputfile = ''
    pastaarvore = ''
    pastaconjunto = ''
    filevalidacao = ''
    fileteste = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:t:d:v:e:o:', ['ifile=', 'tpath=', 'dpath=', 'vfile=', 'efile=', 'ofile='])

    except getopt.GetoptError:
        print('usingPoda.py -i <inputfile> -t <treespath> -d <datasetspath> -v <validationfile> -e <testfile> -o <rulesfile>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingPoda.py -i <inputfile> -t <treespath> -d <datasetspath> -v <validationfile> -e <testfile> -o <rulesfile>\n')
            print('Os parâmetros <inputfile>, <validationfile> e <testfile> DEVEM ser arquivos CSV, já o parâmetro <rulesfile> DEVE ser um TXT. Os parâmetros <treespath> e <datasetspath> DEVEM terminar com /\n')
            print('Exemplo: \n')
            print('usingPoda.py -i \'./poda/conjuntos/adult.csv\' -t \'./poda/arvores/\' -d \'./poda/conjuntos/\' -v \'./poda/saidas/validacao_saida.csv\' -e \'./poda/saidas/teste_saida.csv\' -o \'./poda/saidas/regras_pos_poda.txt\'')
            sys.exit()
        
        elif(opt in ('-i', '--ifile')):
            inputfile = arg
        
        elif(opt in ('-t', '--tpath')):
            pastaarvore = arg

        elif(opt in ('-d', '--dpath')):
            pastaconjunto = arg

        elif(opt in ('-v', '--vfile')):
            filevalidacao = arg
        
        elif(opt in ('-e', '--efile')):
            fileteste = arg

        elif(opt in ('-o', '--ofile')):
            outputfile = arg
        
    
    # Quebra o conjunto em TREINAMENTO, VALIDAÇÃO e TESTES
    # Salva em arquivos na pasta designada
    print('Início da divisão do conjunto: {0}'.format(datetime.now()))

    treinamento, validacao, teste = quebrar_conjunto(
        arquivo_entrada=inputfile
    )

    write_conjunto_no_arquivo(
        conjunto=treinamento,
        arquivo=pastaconjunto+'treinamento.csv'
    )

    write_conjunto_no_arquivo(
        conjunto=validacao,
        arquivo=pastaconjunto+'validacao.csv'
    )

    write_conjunto_no_arquivo(
        conjunto=teste,
        arquivo=pastaconjunto+'teste.csv'
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

    raiz = get_raiz_da_arvore(no=raiz)
    write_arvore_no_arquivo(
        arvore=raiz,
        arquivo=pastaarvore+'arvore_prepoda.json'
    )

    print('Fim da montagem da árvore: {0}'.format(datetime.now()))


    # Podando
    print('Início da poda: {0}'.format(datetime.now()))

    raiz = efetua_poda(
        raiz=raiz,
        validacao=validacao,
        testes=teste,
        deve_escrever_arquivo=True,
        saida_validacao=filevalidacao,
        saida_teste=fileteste
    )

    write_arvore_no_arquivo(
        arvore=raiz,
        arquivo=pastaarvore+'arvore_pospoda.json'
    )

    print('Fim da poda: {0}'.format(datetime.now()))


    print('Início da formulação das regras: {0}'.format(datetime.now()))

    raiz = get_raiz_da_arvore(no=raiz)
    
    dicionario = dict()
    get_dicionario_de_regras(raiz, dicionario, validacao)

    s = processa_impressao(dicionario)
    write_regras(outputfile, s)

    print('Fim da formulação das regras: {0}'.format(datetime.now()))



if(__name__ == '__main__'):
    main(sys.argv[1:])
