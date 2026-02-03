import pandas as pd
import os
import io

CADOP_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

def enrich_data_with_cadop(df_despesas):
    """
    Realiza o download do CADOP, SALVA O ARQUIVO LIMPO (requisito Teste 3)
    e faz o Left Join com as despesas.
    Retorna o DataFrame enriquecido com UF e Modalidade.
    """
    print("  -> [ENRICHER] Baixando e processando CADOP...")
    
    try:
        # 1. Download e Leitura com Estratégia de Encoding
        # Tenta UTF-8 primeiro (Padrão Web). Se der erro, tenta Latin-1.
        try:
            cadop = pd.read_csv(CADOP_URL, sep=';', encoding='utf-8', dtype=str, on_bad_lines='skip')
        except UnicodeDecodeError:
            print("     [INFO] UTF-8 falhou. Tentando Latin-1...")
            cadop = pd.read_csv(CADOP_URL, sep=';', encoding='latin1', dtype=str, on_bad_lines='skip')
        except Exception:
            # Fallback final para 'cp1252' (comum no Windows)
            cadop = pd.read_csv(CADOP_URL, sep=';', encoding='cp1252', dtype=str, on_bad_lines='skip')

        # 2. Normalização de Colunas
        cadop.columns = cadop.columns.str.strip().str.upper()
        
        # 3. Busca dinâmica de colunas (Resiliência contra mudança de nomes)
        try:
            col_cnpj = next(c for c in cadop.columns if 'CNPJ' in c)
            col_reg = next(c for c in cadop.columns if 'REGISTRO' in c)
            col_uf = next(c for c in cadop.columns if 'UF' in c)
            col_mod = next(c for c in cadop.columns if 'MODALIDADE' in c)
            col_razao = next(c for c in cadop.columns if 'RAZAO' in c) # Adicionado para o Teste 3
        except StopIteration:
            print("     [ERRO] Colunas esperadas do CADOP não encontradas. Pulando enriquecimento.")
            df_despesas['UF'] = 'N/I'
            df_despesas['Modalidade'] = 'Desconhecida'
            return df_despesas

        # 4. Limpeza e Seleção
        cadop_clean = cadop[[col_cnpj, col_reg, col_razao, col_uf, col_mod]].copy()
        cadop_clean.columns = ['CNPJ', 'RegistroANS', 'RazaoSocial', 'UF', 'Modalidade']
        
        # Remove não numéricos do CNPJ para garantir o match
        cadop_clean['CNPJ'] = cadop_clean['CNPJ'].str.replace(r'\D', '', regex=True)
        
        # Remove duplicatas (mantém a primeira ocorrência encontrada)
        cadop_clean = cadop_clean.drop_duplicates(subset=['CNPJ'])

        # Calcula o caminho da pasta 'data' dentro do módulo 2 (sobe um nível de src/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, 'data', 'operadoras_ativas.csv')
        
        print(f"  -> [ENRICHER] Salvando CSV de operadoras para Teste 3 em: {output_path}")
        # Salvamos com encoding utf-8-sig para evitar problemas no SQL depois
        cadop_clean.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')

        # 5. Preparação da chave no DF principal
        df_despesas['CNPJ_Clean'] = df_despesas['CNPJ'].str.replace(r'\D', '', regex=True)

        # 6. O JOIN (Left)
        print("  -> [ENRICHER] Cruzando tabelas (Merge)...")
        # Fazemos o merge apenas com as colunas necessárias para o enriquecimento
        df_merged = df_despesas.merge(
            cadop_clean[['CNPJ', 'RegistroANS', 'UF', 'Modalidade']], 
            left_on='CNPJ_Clean', 
            right_on='CNPJ', 
            how='left', 
            suffixes=('', '_cadop')
        )
        
        # 7. Fallback para nulos (Preenche quem não deu match)
        df_merged['UF'] = df_merged['UF'].fillna('N/I')
        df_merged['Modalidade'] = df_merged['Modalidade'].fillna('Desconhecida')

        # Limpeza da coluna auxiliar usada apenas para o join
        if 'CNPJ_Clean' in df_merged.columns:
            df_merged.drop(columns=['CNPJ_Clean'], inplace=True)
            
        return df_merged

    except Exception as e:
        print(f"     [ERRO CRÍTICO] Falha no enriquecimento: {e}")
        # Retorna o original para não quebrar o pipeline
        return df_despesas