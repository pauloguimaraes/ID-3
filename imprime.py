
def imprime_arvore(raiz):
    for filho in raiz.children:
        if(not filho.is_leaf):
            imprime_arvore(filho)
        else:
            get_regras(filho)

def get_regras(no):
    string = 'IF ({0}'.format(str(no.path[0].name).replace('/', ''))

    i = 0
    for n in no.path[1:]:
        i = i + 1
        string = string + (' == {0}'.format(n.attribute))
        if(i == len(no.path)-1):
            string = string + ') THEN {0}'.format(n.classe_major)
        else:
            string = string + ' AND {0}'.format(n.name)
    print(string)
    print()

def imprime(no, string_atual):
    # print(len(no.anchestors))
    # i_tmp = len(no.anchestors)-1

    # while(i_tmp > 0):
    #     i_tmp = i_tmp - 1
    #     string_atual = string_atual + '\t'

    for filho in no.children:
        i = len(no.anchestors)
        while(i > 0):
            i = i - 1
            string_atual = string_atual + '\t'

        string_atual = string_atual + 'IF {0} == {1} THEN '.format(no.name, filho.attribute)

        if(filho.is_leaf):
            string_atual = string_atual + filho.classe_major
        string_atual = string_atual + '\n'

        string_atual = imprime(filho, string_atual)
        

    return string_atual