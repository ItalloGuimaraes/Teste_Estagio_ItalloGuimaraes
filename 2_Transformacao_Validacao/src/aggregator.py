import pandas as pd

def calculate_statistics(df):
    """
    Agrupa por RazaoSocial, RegistroANS, Modalidade e UF e calcula:
    - Soma (Total Despesas)
    - Média Trimestral
    - Desvio Padrão
    """
    print("  -> [AGGREGATOR] Calculando Estatísticas...")

    # Garante preenchimento de nulos nas colunas de agrupamento
    fill_values = {
        'UF': 'N/I',
        'RegistroANS': 'N/I',
        'Modalidade': 'Desconhecida'
    }
    df.fillna(fill_values, inplace=True)

    # Definição das colunas que identificam unicamente a operadora no grupo
    group_cols = ['RazaoSocial', 'RegistroANS', 'Modalidade', 'UF']

    # Definição das agregações
    agg_cols = {'Valor Despesas': ['sum', 'mean', 'std', 'count']}
    
    # GroupBy
    resultado = df.groupby(group_cols).agg(agg_cols).reset_index()
    
    # Achatando as colunas (MultiIndex -> Colunas simples)
    # A ordem aqui tem que bater com group_cols + agg_cols
    resultado.columns = [
        'RazaoSocial', 'RegistroANS', 'Modalidade', 'UF', 
        'Despesa_Total', 'Media_Trimestral', 'Desvio_Padrao', 'Qtd_Registros'
    ]
    
    # Tratamento final (Arredondamento e NaNs no desvio padrão)
    resultado['Despesa_Total'] = resultado['Despesa_Total'].round(2)
    resultado['Media_Trimestral'] = resultado['Media_Trimestral'].round(2)
    resultado['Desvio_Padrao'] = resultado['Desvio_Padrao'].round(2).fillna(0.0) 

    # Ordenação
    resultado = resultado.sort_values(by='Despesa_Total', ascending=False)
    
    return resultado