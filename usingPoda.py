


from datetime import datetime
from treinaModelo import quebrar_conjunto
from arvore import get_raiz_do_conjunto, get_classe_majoritaria, monta_arvore
from poda import efetua_poda
import sys, getopt



def main(argv):
    """
    Função de execução
    """

    inputfile = ''
    pastaarvore = ''
    pastaconjunto = ''
    filetreinamento = ''
    fileteste = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:t:d:', ['ifile=', 'tpath=', 'dpath='])

    except getopt.GetoptError:
        print('usingGeraGrafico.py -i <inputfile> -t <treespath> -d <datasetspath> -n <trainfile> -e <testfile>')
        sys.exit(2)

    for opt, arg in opts:
        if(opt == '-h'):
            print('usingGeraGrafico.py -i <inputfile> -t <treespath> -d <datasetspath> -n <trainfile> -s <testfile>\n')
            print('Os parâmetros <inputfile>, <trainfile> e <testfile> DEVEM ser arquivos CSV. Os parâmetros <treespath> e <datasetspath> DEVEM terminar com /\n')
            print('Exemplo: \n')
            print('usingGeraGrafico.py -i \'./files/grafico/datasets/adult.csv\' -t \'./files/grafico/trees/\' -d \'./files/grafico/datasets/\' -n \'./files/grafico/output/treinamento_saida.csv\' -e \'./files/grafico/output/teste_saida.csv\'')
        
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
        
    print('Início da divisão do conjunto: {0}'.format(datetime.now()))

    treinamento, validacao, teste = quebrar_conjunto(
        arquivo_entrada=inputfile
    )

    print('Fim da divisão do conjunto: {0}'.format(datetime.now()))

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

    print('Fim da montagem da árvore: {0}'.format(datetime.now()))

    raiz = efetua_poda(raiz=raiz, validacao=validacao, testes=teste, deve_escrever_arquivo=True, saida_validacao='./validacao.csv', saida_teste='./testes.csv')



if(__name__ == '__main__'):
    main(sys.argv[1:])
