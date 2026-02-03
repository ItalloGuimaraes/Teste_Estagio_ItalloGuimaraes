import re

#  Valida CNPJ utilizando o cálculo dos dígitos verificadores.
def validate_cnpj(cnpj: str) -> bool:
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', str(cnpj))
    
    # Verifica tamanho e sequências inválidas conhecidas (ex: 00000000000000)
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    # Cálculo do primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    digito1 = 11 - (soma1 % 11)
    digito1 = 0 if digito1 >= 10 else digito1

    if digito1 != int(cnpj[12]):
        return False

    # Cálculo do segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma2 = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    digito2 = 11 - (soma2 % 11)
    digito2 = 0 if digito2 >= 10 else digito2

    return digito2 == int(cnpj[13])