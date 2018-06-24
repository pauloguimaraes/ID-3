"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Execução do treinamento e gerando CSV com a acurácia da árvore enquanto treina
"""



# Módulos necessários
from arvore import get_classe_majoritaria, get_raiz_da_arvore, get_raiz_do_conjunto, monta_arvore
from datetime import datetime
from manipulacaoArquivos import write_arvore_no_arquivo, write_conjunto_no_arquivo
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
    filetreinamento = ''
    fileteste = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:t:d:n:e:', ['ifile=', 'tpath=', 'dpath=', 'nfile=', 'efile='])

    except getopt.GetoptError:
        print('usingGeraGrafico.py -i <inputfile> -t <treespath> -d <datasetspath> -n <trainfile> -e <testfile>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingGeraGrafico.py -i <inputfile> -t <treespath> -d <datasetspath> -n <trainfile> -e <testfile>\n')
            print('Os parâmetros <inputfile>, <trainfile> e <testfile> DEVEM ser arquivos CSV. Os parâmetros <treespath> e <datasetspath> DEVEM terminar com /\n')
            print('Exemplo: \n')
            print('usingGeraGrafico.py -i \'./files/grafico/datasets/adult.csv\' -t \'./files/grafico/trees/\' -d \'./files/grafico/datasets/\' -n \'./files/grafico/output/treinamento_saida.csv\' -e \'./files/grafico/output/teste_saida.csv\'')
            sys.exit()
        
        elif(opt in ('-i', '--ifile')):
            inputfile = arg
        
        elif(opt in ('-t', '--tpath')):
            pastaarvore = arg

        elif(opt in ('-d', '--dpath')):
            pastaconjunto = arg

        elif(opt in ('-n', '--nfile')):
            filetreinamento = arg
        
        elif(opt in ('-e', '--efile')):
            fileteste = arg
    

    # Quebra o conjunto de TREINAMENTO, VALIDAÇÃO e TESTES
    # Escreve os três conjuntos em arquivos
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


    # Gera a árvore de treinamento
    # Vai gerando CSV com desempenho dos conjuntos de treinamento e testes diante do modelo
    # Salva a árvore em um JSON
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
        arquivo_saida_treinamento=filetreinamento,
        arquivo_saida_testes=fileteste,
        deve_testar_enquanto_monta=False
    )

    raiz = get_raiz_da_arvore(raiz)
    write_arvore_no_arquivo(
        arvore=raiz,
        arquivo=pastaarvore+'arvore_gerada.json'
    )

    print('Fim da montagem da árvore: {0}'.format(datetime.now()))



if(__name__ == '__main__'):
    main(sys.argv[1:])
