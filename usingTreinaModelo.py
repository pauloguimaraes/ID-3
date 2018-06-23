import sys, getopt
from treinaModelo import treina


def main(argv):
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

        raiz = treina(
            arquivo_entrada=inputfile,
            arvore_gerada=outputfile+'.json'
        )


if(__name__ == '__main__'):
    main(sys.argv[1:])