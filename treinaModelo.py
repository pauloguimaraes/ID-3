from arvore import get_classe_majoritaria, get_raiz_do_conjunto, monta_arvore
from preProcessamento import trata_conjunto
from manipulacaoArquivos import write_arvore_no_arquivo



def treina(arquivo_entrada, arvore_gerada):
    conjunto = trata_conjunto(
        arquivo_entrada=arquivo_entrada,
        char_a_remover='?',
        numero_de_grupos=3
    )

    raiz = get_raiz_do_conjunto(
        conjunto=conjunto
    )
    classe_majoritaria = get_classe_majoritaria(
        conjunto=conjunto
    )
    monta_arvore(
        conjunto_completo=conjunto,
        conjunto_atual=conjunto,
        conjunto_teste=conjunto,
        raiz=raiz,
        nome_da_raiz=raiz.name,
        classe_majoritaria=classe_majoritaria
    )

    write_arvore_no_arquivo(
        arvore=raiz,
        arquivo=arvore_gerada
    )

    return raiz