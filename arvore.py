"""
Exercício de Programação de Inteligência Artificial
Professora Doutora Patrícia Rufino Oliveira

Autores:
Lucas Borelli Amaral                9360951
Paulo Henrique Freitas Guimarães    9390361
Silas Rocha Pereira                 9424079
Victor Taendy Sousa                 8921421

Módulo responsável por trabalhar com a estrutura da árvore
"""



# Módulos necessários
from anytree import Node
from calculos import ganho
from manipulacaoArquivos import write_saida



def get_numero_de_nos(arvore):
    """
    Retorna o número de nós presentes na subárvore @arvore
    """

    quantidade = 0

    for descendente in arvore.descendants:
        # Não contamos as folhas como nós pois elas armazenam as classes
        if(descendente.is_leaf):
            continue
        quantidade = quantidade + 1

    return quantidade + 1



def is_no_de_decisao(no):
    """
    Retorna se o @no eh um nó de decisão em sua @arvore
    """

    eh = True

    # Uma folha não é um nó de decisão
    if(no.is_leaf):
        return False

    # Se ao menos um dos filhos não for folha então não é um nó de decisão
    for filho in no.children:
        if(filho.is_leaf):
            continue
        
        eh = False
        break
    
    return eh



def get_raiz_da_arvore(no):
    """
    Recupera a raiz do @no
    """

    # Retorna o próprio nó se ele for a raiz
    if(no.is_root):
        return no

    # Senão percorre todos os ancestrais até encontrar a raiz
    no_raiz = Node(name='')
    for ancestral in no.anchestors:
        if(ancestral.is_root):
            no_raiz = ancestral
            break
    
    return no_raiz



def get_raiz_do_conjunto(conjunto):
    """
    Recupera o nó raiz do @conjunto, calculando, naturalmente, o ganho para todos os atributos e retornando o melhor
    """

    ganhos = dict()

    for coluna in conjunto:
        if(coluna == 'label'):
            continue

        ganhos[coluna] = ganho(
            conjunto=conjunto,
            atributo=coluna,
            rotulo='label'
        )

    ganhos_ordenados = sorted(
        ganhos.items(),
        key=lambda x: x[1],
        reverse=True
    )

    classe_majoritaria = get_classe_majoritaria(conjunto)
    raiz = ganhos_ordenados[0][0]
    return Node(
        name=raiz,
        attribute=None,
        classe_major=classe_majoritaria
    )



def get_classe_majoritaria(conjunto):
    """
    Recupera a classe majoritária do @conjunto
    """
    
    classes = set(conjunto['label'])
    ocorrencias = dict()

    for classe in classes:
        ocorrencias[classe] = len(conjunto[(conjunto['label'] == classe)])

    ocorrencias_ordenadas = sorted(
        ocorrencias.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ocorrencias_ordenadas[0][0]



def verifica_exemplo_no_modelo(exemplo, arvore):
    """
    Testa o @exemplo dado o modelo treinado na @arvore
    """

    nome = arvore.name

    if(arvore.is_leaf):
        return arvore.classe_major

    for item in arvore.children:
        if(exemplo[nome].strip() == item.attribute.strip()):
            
            return verifica_exemplo_no_modelo(
                exemplo=exemplo,
                arvore=item
            )
        else:
            continue
        
    # Se não encontrou nenhum valor
    # Retorna a classe majoritária da raiz
    return get_raiz_da_arvore(arvore).classe_major



def get_acuracia(conjunto, modelo):
    # pylint: disable=W0612
    """
    Executa o teste do @conjunto diante do @modelo recuperando a acurácia
    """

    acertos = 0

    for indice, linha in conjunto.iterrows():
        predicao = verifica_exemplo_no_modelo(linha, modelo)
        valor_correto = linha['label'].replace('.', '').strip()

        if(predicao == valor_correto):
            acertos = acertos + 1

    n_elementos = len(conjunto)
    pct_acertos = acertos / n_elementos
    return pct_acertos



def get_erro(conjunto, arvore):
    """
    Retorna o erro do @conjunto diante do modelo treinado na @arvore
    """

    if(len(conjunto) <= 0):
        return 0

    erro_deste_teste = 1 - get_acuracia(conjunto=conjunto, modelo=arvore)
    return erro_deste_teste



def monta_arvore(conjunto_completo, conjunto_atual, conjunto_teste, raiz, nome_da_raiz, classe_majoritaria, arquivo_saida_treinamento, arquivo_saida_testes, deve_testar_enquanto_monta=False):
    """
    Monta recursivamente uma árvore de decisão para o @conjunto_atual.

    Usa como base os valores do @conjunto_completo, pois o conjunto vai sendo replicado e reduzido pela árvore conforme vamos descendo.
    Os nós têm o @name representando o valor que faz chegar até esse nó, o @attribute representando qual o próximo atributo a ser analisado e o @classe_major representando a classe majoritária identificada para esse nó.
    
    O nó @raiz é o atributo pai do atual nível da árvore
    """

    # Usa o conjunto completo para recuperar os possíveis valores
    # Dessa forma a árvore não fica incompleta caso não tenhamos exemplos com determinado valor
    conjunto_de_valores_possiveis = set(conjunto_completo[nome_da_raiz])


    # Se deve montar testando a árvore
    if(deve_testar_enquanto_monta):
        # Recupera a raiz
        raiz_temp = get_raiz_da_arvore(raiz)

        # Mensura a acurácia para o conjunto de treinamento
        acuracia_treinamento = get_acuracia(
            conjunto=conjunto_completo,
            modelo=raiz_temp
        )

        # Mensura a acurácia para o conjunto de testes
        acuracia_testes = get_acuracia(
            conjunto=conjunto_teste,
            modelo=raiz_temp
        )

        # Escreve nos arquivos de saída
        write_saida(
            acuracia=acuracia_testes,
            arquivo=arquivo_saida_testes,
            numero_nos=get_numero_de_nos(raiz_temp)
        )

        write_saida(
            acuracia=acuracia_treinamento,
            arquivo=arquivo_saida_treinamento,
            numero_nos=get_numero_de_nos(raiz_temp)
        )
    
    # Para todos os valores possíveis que o atributo possa assumir
    for valor in conjunto_de_valores_possiveis:

        # Cria-se um conjunto de dados temporário com apenas exemplos com o valor atual
        conjunto_temporario = conjunto_atual[(conjunto_atual[nome_da_raiz] == valor)]
        conjunto_temporario = conjunto_temporario.reset_index(drop=True)

        # Lista-se os rótulos possíveis desses exemplos
        rotulos_possiveis = list(set(conjunto_temporario['label']))
        quantidade_rotulos_possiveis = len(rotulos_possiveis)

        # Se só há um rótulo possível então não existem mais decisões a serem tomadas
        if(quantidade_rotulos_possiveis == 1):
            Node(
                name='',
                attribute=valor,
                classe_major=rotulos_possiveis[0],
                parent=raiz
            )

        # Se não há nenhum rótulo possível então retorna a classe majoritária do pai
        elif(quantidade_rotulos_possiveis == 0):
            Node(
                name='',
                attribute=valor,
                classe_major=classe_majoritaria,
                parent=raiz
            )

        # Se temos exemplos de ambas as classes
        else:
            ganhos = dict()

            # Para todos os atributos possíveis precisaresmos calcular os ganhos
            for coluna in conjunto_temporario:
                # Exceto para o rótulo e para o próprio atributo
                if(coluna == 'label' or coluna == nome_da_raiz):
                    continue

                ganhos[coluna] = ganho(
                    conjunto=conjunto_temporario,
                    atributo=coluna,
                    rotulo='label'
                )
            
            # Ordena os ganhos de forma a recuperar o melhor
            ganhos_ordenados = sorted(
                ganhos.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # Se existem ganhos calculados
            if(len(ganhos_ordenados) > 0):
                # Remove o atributo que estávamos analisando e passa o conjunto pra frente
                conjunto_temporario = conjunto_temporario.drop(columns=
                [nome_da_raiz])
                
                classe_majoritaria = get_classe_majoritaria(conjunto_temporario)

                no = Node(
                    name=ganhos_ordenados[0][0],
                    attribute=valor,
                    classe_major=classe_majoritaria,
                    parent=raiz
                )
                monta_arvore(
                    conjunto_completo=conjunto_completo,
                    conjunto_atual=conjunto_temporario,
                    conjunto_teste=conjunto_teste,
                    raiz=no,
                    nome_da_raiz=no.name,
                    classe_majoritaria=classe_majoritaria,
                    arquivo_saida_treinamento=arquivo_saida_treinamento,
                    arquivo_saida_testes=arquivo_saida_testes,
                    deve_testar_enquanto_monta=deve_testar_enquanto_monta
                )
                
            # Se existem elementos nesse subconjunto retorna a classe majoritária
            elif(len(conjunto_temporario) > 0):
                classe_majoritaria = get_classe_majoritaria(conjunto_temporario)
                
                Node(
                    name='',
                    attribute=valor,
                    classe_major=classe_majoritaria,
                    parent=raiz
                )
            
            # Se não existem retorna-se a classe majoritária do pai
            else:
                Node(
                    name='',
                    attribute=valor,
                    classe_major=classe_majoritaria,
                    parent=raiz
                )


