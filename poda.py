"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa                 8921421

Módulo com métodos relacionados à poda (Reduced-Error Prunning)
"""



# Módulos necessários
from anytree import Node
from arvore import get_classe_majoritaria, get_erro, is_no_de_decisao, get_numero_de_nos, get_raiz_da_arvore, remove_no



def poda(no, validacao, classe_majoritaria):
    """
    Efetua a remoção do @no e o teste com os conjuntos de @validacao.

    Usa a @classe_majoritaria do subconjunto de validação para definir a classe do novo nó folha
    Caso o conjunto esteja vazio usa a classe majoritária do nó pai.
    """

    # Se o conjunto estiver vaiz retorna-se o erro total da árvore para esse nó
    major = classe_majoritaria
    if(len(validacao) <= 0):
        return [get_erro(conjunto=validacao, arvore=get_raiz_da_arvore(no)), major]

    # Senão retorna o erro com o novo nó folha
    antiga_major = no.classe_major
    major = get_classe_majoritaria(validacao)
    no.classe_major = major
    
    # Realoca os filhos para um nó temporário
    no_temp = Node(name='')
    for filho in no.children:
        filho.parent = no_temp

    # Calcula o erro
    raiz = get_raiz_da_arvore(no)
    erro_pos_poda_validacao = get_erro(conjunto=validacao, arvore=raiz)
    
    # Realoca os filhos para o nó
    # O nó somente será removido de fato mais para frente
    for filho in no_temp.children:
        filho.parent = no
    
    no.classe_major = antiga_major

    # Retorna-se o erro pós-poda e a nova classe majoritária desse nó
    return [erro_pos_poda_validacao, major]



def get_erros_para_a_arvore(raiz, validacao, testes, erros=dict(), novas_classes_majoritarias=dict()):
    """
    Recupera conjuntos de @erros e @novas_classes_majoritarias para os nós removidos.

    Usa a @raiz da árvore e o conjunto de @validacao para poda e @testes para testes.
    O conjunto de erros depois será utilizado para a remoção de fato dos nós.
    """

    subconjunto_validacao = validacao

    for filho in raiz.children:
        # Se for um nó de decisão
        if(is_no_de_decisao(filho)):
            # Extrai as regras que fazem chegar nele
            no = filho
            while(no.attribute != None):
                # Filtra o conjunto de validação
                subconjunto_validacao = subconjunto_validacao[(subconjunto_validacao[no.parent.name] == no.attribute)]

                no = no.parent

            # Recupera a classe majoritária do conjunto de validação
            classe_majoritaria_validacao = get_classe_majoritaria(
                conjunto=validacao
            )
            # Recupera-se o erro do conjunto
            resultado = poda(
                no=filho,
                validacao=subconjunto_validacao,
                classe_majoritaria=classe_majoritaria_validacao
            )
            erros[filho]=resultado[0]
            novas_classes_majoritarias[filho]=resultado[1]
            break
        
        # Se não é um nó de decisão desce na árvore
        else:
            get_erros_para_a_arvore(
                raiz=filho,
                validacao=validacao,
                testes=testes,
                erros=erros,
                novas_classes_majoritarias=novas_classes_majoritarias
            )



def efetua_poda(raiz, validacao, testes, deve_escrever_arquivo=True, saida_teste='./poda/saida/teste.csv', saida_validacao='./poda/saida/validacao.csv'):
    # Calculam-se os erros pré-poda
    erro_pre_poda_teste = get_erro(conjunto=testes, arvore=raiz)
    erro_pre_poda_validacao = get_erro(conjunto=validacao, arvore=raiz)

    numero_de_nos = get_numero_de_nos(raiz)

    # Se deve escrever no arquivo então anota a acurácia e o número de nós
    # Formato CSV
    if(deve_escrever_arquivo):
        out_testes = 'acuracia, n_nos' + '\n'
        out_valida = 'acuracia, n_nos' + '\n'

        out_testes = out_testes + '{0}, {1}'.format((1-erro_pre_poda_teste), numero_de_nos) + '\n'
        out_valida = out_valida + '{0}, {1}'.format((1-erro_pre_poda_validacao), numero_de_nos) + '\n'

        with open(saida_teste, 'a') as obj_file:
            obj_file.write(out_testes)

        with open(saida_validacao, 'a') as obj_file:
            obj_file.write(out_valida)
    

    menor_erro_valor = 0
    validacao_completo = validacao

    # Entquanto o menor erro encontrado for menor que o erro pré-poda deve-se podar
    while(menor_erro_valor <= erro_pre_poda_validacao):
        print('Erro pré-poda: {0}'.format(erro_pre_poda_validacao))

        erros = dict()
        novas_classes_majoritarias = dict()

        # Recupera os conjuntos de erro e de novas classes majoritárias
        get_erros_para_a_arvore(
            raiz=raiz,
            validacao=validacao,
            testes=testes,
            erros=erros,
            novas_classes_majoritarias=novas_classes_majoritarias
        )

        # Ordena os erros de forma a recuperar o menor
        erros_ordenados = sorted(
            erros.items(),
            key=lambda x: x[1]
        )
        menor_erro_valor = erros_ordenados[0][1]

        print('Menor erro encontrado: {0}'.format(menor_erro_valor))

        # Percorre todos os erros
        for no, valor in erros_ordenados:
            # Se for menor que o erro pré-poda remove
            if(valor <= erro_pre_poda_validacao):
                raiz = remove_no(no, novas_classes_majoritarias[no])
        
        # Calcula o erro pós poda para validação e teste
        raiz = get_raiz_da_arvore(raiz)
        erro_pos_poda_teste = get_erro(conjunto=testes, arvore=raiz)
        erro_pos_poda_validacao = get_erro(conjunto=validacao_completo, arvore=raiz)

        # O novo erro pré-poda é o erro pós-poda calculado
        erro_pre_poda_teste = erro_pos_poda_teste
        erro_pre_poda_validacao = erro_pos_poda_validacao
        print('Erro pós-poda: {0}'.format(erro_pos_poda_validacao))

        # Escreve a poda no arquivo de acurácia
        if(deve_escrever_arquivo):
            contagem = get_numero_de_nos(raiz)

            out_testes = '{0}, {1}'.format((1-erro_pos_poda_teste), contagem) + '\n'
            out_valida = '{0}, {1}'.format((1-erro_pos_poda_validacao), contagem) + '\n'

            with open(saida_teste, 'a') as obj_file:
                obj_file.write(out_testes)

            with open(saida_validacao, 'a') as obj_file:
                obj_file.write(out_valida)

    return get_raiz_da_arvore(raiz)


