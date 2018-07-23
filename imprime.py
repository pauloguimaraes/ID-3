"""
Exercicio de Programacao de Inteligencia Artificial
Professora Doutora Patricia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimaraes    9390361
Silas Rocha Pereira da Silva        9424079
Victor Taendy Sousa Emerenciano     8921412

Impressão da árvore como um conjunto de regras
"""



def get_dicionario_de_regras(raiz, dic, conjunto):
    """
    Preenche o @dic com as regras de cada nó folha da @raiz, usando o @conjunto para definir a cobertura
    """

    # Preenche todas as folhas
    for filho in raiz.children:

        # Se não for folha chama recursivamente para o filho
        if(not filho.is_leaf):
            get_dicionario_de_regras(filho, dic, conjunto)

        # Senão, manipula a estrutura do Anytree para preencher como regras
        else:
            regras = get_regras(filho).replace(') THEN', ' ;').replace('IF (', '').strip()
            conj_regras = regras.split(' AND ')

            conj_tmp = conjunto

            # Separa as igualdades de forma a conseguir uma chave (atributo) e valor
            for regra in conj_regras:
                attVal = regra.split(' == ')
                att = attVal[0]
                val = attVal[1].split(';')[0].strip()

                conj_tmp = conj_tmp[(conj_tmp[att] == val)]
            
            dic[regras] = len(conj_tmp)



def processa_impressao(dicionario):
    """
    Processa o @dicionario de forma a montar uma string com as regras
    """
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
        string = string + '{0} [Cobertura: {1}])'.format(chave.replace('; >50K', '').strip(), dic_no[chave])

        i = i + 1
        if(i < len(dic_no)):
            string = string + ' OR \n\t('

    string = string + '\n THEN >50K'
    return string



def get_regras(no):
    """
    Recupera a regra do @no em formato legível
    """
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
