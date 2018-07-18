
def imprime_arvore(raiz, dic, conjunto):
    for filho in raiz.children:
        if(not filho.is_leaf):
            imprime_arvore(filho, dic, conjunto)
        else:
            regras = get_regras(filho).replace(') THEN', ' ;').replace('IF (', '').strip()
            conj_regras = regras.split(' AND ')

            conj_tmp = conjunto
            for regra in conj_regras:
                attVal = regra.split(' == ')
                att = attVal[0]
                val = attVal[1].split(';')[0].strip()

                conj_tmp = conj_tmp[(conj_tmp[att] == val)]
            
            dic[regras] = len(conj_tmp)


def processa_impressao(dicionario):
    sort = sorted(
        dicionario.items(),
        key=lambda x: x[1],
        reverse=True
    )

    sort_as_dict = dict()
    for item in sort:
        sort_as_dict[item[0]] = item[1]

    dic_yes = dict((key, value) for key, value in sort_as_dict.items() if key.find('; <=50K') > 0)
    dic_no = dict((key, value) for key, value in sort_as_dict.items() if key.find('; >50K') > 0)

    string = 'IF \n\t('
    i = 0
    for chave in dic_yes:
        string = string + '{0} [Cobertura: {1}])'.format(chave.replace('; <=50K', '').strip(), dic_yes[chave])
        
        i = i + 1

        if(i < len(dic_yes)):
            string = string + ' OR \n\t('

    string = string + '\n THEN <=50K\nELSE IF\n\t'

    i = 0
    for chave in dic_no:
        string = string + '({0} [Cobertura: {1}])'.format(chave.replace('; >50K', '').strip(), dic_no[chave])

        i = i + 1
        if(i < len(dic_no)):
            string = string + ' OR \n('

    string = string + '\n THEN >50K'
    # print(string)
    return string

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

    return string

# # def imprime(no, string_atual):
# #     # print(len(no.anchestors))
# #     # i_tmp = len(no.anchestors)-1

# #     # while(i_tmp > 0):
# #     #     i_tmp = i_tmp - 1
# #     #     string_atual = string_atual + '\t'

# #     for filho in no.children:
# #         i = len(no.anchestors)
# #         while(i > 0):
# #             i = i - 1
# #             string_atual = string_atual + '\t'

# #         string_atual = string_atual + 'IF {0} == {1} THEN '.format(no.name, filho.attribute)

# #         if(filho.is_leaf):
# #             string_atual = string_atual + filho.classe_major
# #         string_atual = string_atual + '\n'

# #         string_atual = imprime(filho, string_atual)
        

# #     return string_atual