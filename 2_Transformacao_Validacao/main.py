import pandas as pd
import os
import sys
import zipfile

# Adiciona src ao path para importar os módulos vizinhos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from validator import validate_cnpj
from enricher import enrich_data_with_cadop
from aggregator import calculate_statistics

# CONFIGURAÇÃO
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TESTE_1 = os.path.join(CURRENT_DIR, '..', '1_Leitura_Transformacao_Dados')
FILE_NAME = "consolidado_despesas.csv"
ZIP_NAME = "consolidado_despesas.zip"
OUTPUT_FILE = os.path.join(CURRENT_DIR, "despesas_agregadas.csv")

# Busca inteligente do input (CSV ou ZIP) nas pastas.
def get_input_dataframe():
    possible_paths = [
        os.path.join(CURRENT_DIR, 'data', FILE_NAME),
        os.path.join(PATH_TESTE_1, FILE_NAME)
    ]
    for p in possible_paths:
        if os.path.exists(p):
            print(f"  -> Arquivo encontrado: {p}")
            return pd.read_csv(p, sep=';', encoding='utf-8-sig', dtype=str)

    zip_path = os.path.join(PATH_TESTE_1, ZIP_NAME)
    if os.path.exists(zip_path):
        print(f"  -> ZIP encontrado no Teste 1: {zip_path}. Extraindo...")
        with zipfile.ZipFile(zip_path) as z:
            with z.open(FILE_NAME) as f:
                return pd.read_csv(f, sep=';', encoding='utf-8-sig', dtype=str)
    
    raise FileNotFoundError("Input não encontrado no Teste 1 ou localmente.")

def main():
    print("========================================================")
    print(" INICIANDO TESTE 2: TRANSFORMAÇÃO E VALIDAÇÃO DE DADOS")
    print("========================================================")
    
    # 1. Carregamento
    try:
        df = get_input_dataframe()
    except Exception as e:
        print(f"[ERRO] {e}"); return

    # Conversão Monetária
    print("  -> Convertendo valores monetários...")
    df['Valor Despesas'] = pd.to_numeric(df['Valor Despesas'].str.replace(',', '.'), errors='coerce').fillna(0.0)

    # 2. Validação (Usa src/validator.py)
    print("  -> Executando Validação de CNPJs...")
    df['CNPJ_Valido'] = df['CNPJ'].apply(validate_cnpj)
    
    invalidos = len(df[~df['CNPJ_Valido']])
    if invalidos > 0:
        print(f"     [ALERTA] Encontrados {invalidos} registros com CNPJ matematicamente inválido.")

    # 3. Enriquecimento (Usa src/enricher.py)
    df_enriched = enrich_data_with_cadop(df)

    # 4. Agregação (Usa src/aggregator.py)
    df_final = calculate_statistics(df_enriched)

    # 5. Salvamento
    print(f"  -> Salvando resultado em: {OUTPUT_FILE}")
    df_final.to_csv(OUTPUT_FILE, index=False, sep=';', encoding='utf-8-sig')

    print("\n======================================================")
    print("   SUCESSO! Arquivo 'despesas_agregadas.csv' gerado.")
    print("======================================================")

if __name__ == "__main__":
    main()