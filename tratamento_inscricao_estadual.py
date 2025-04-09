#Função para colocar 0's caso o iestadual tenha menos de 9 numeros

def inscricao_estadual_zero_inicio(iestadual):
    if len(iestadual) == 7:
        iestadual = '00' + iestadual
    elif len(iestadual) == 8:
        iestadual = '0' + iestadual
    return iestadual

    