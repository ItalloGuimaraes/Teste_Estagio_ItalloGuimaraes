import pandas as pd
import os
import sys

class DataService:
    def __init__(self):
        self.df_ops = pd.DataFrame()
        self.df_desp = pd.DataFrame()
        self.df_agg = pd.DataFrame()
        self._load_data()

    # Carrega os dados dos módulos anteriores para a memória.
    def _load_data(self):
        try:
            # Caminho base: sobe 3 níveis a partir deste arquivo para achar a raiz
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            path_ops = os.path.join(BASE_DIR, '2_Transformacao_Validacao', 'data', 'operadoras_ativas.csv')
            path_desp = os.path.join(BASE_DIR, '1_Leitura_Transformacao_Dados', 'consolidado_despesas.csv')
            path_agg = os.path.join(BASE_DIR, '2_Transformacao_Validacao', 'despesas_agregadas.csv')

            print(f"Carregando dados de: {BASE_DIR}")

            # ---------------------------
            # 1. CARGA DE OPERADORAS
            # ---------------------------
            if os.path.exists(path_ops):
                self.df_ops = pd.read_csv(path_ops, sep=';', encoding='utf-8', dtype=str)
                self.df_ops.fillna('', inplace=True)
                # Normaliza colunas para evitar erros de Case Sensitive
                self.df_ops.columns = [c.strip().upper() for c in self.df_ops.columns]
                # Garante que temos as chaves principais
                if 'REGISTROANS' not in self.df_ops.columns and 'REGISTRO' in self.df_ops.columns:
                    self.df_ops.rename(columns={'REGISTRO': 'REGISTROANS'}, inplace=True)
            else:
                print(f"⚠️ AVISO: Arquivo de Operadoras não encontrado: {path_ops}")

            # ---------------------------
            # 2. CARGA DE DESPESAS 
            # ---------------------------
            if os.path.exists(path_desp):
                # Lê tudo como string primeiro para segurança
                try:
                    self.df_desp = pd.read_csv(path_desp, sep=';', encoding='utf-8', dtype=str)
                except UnicodeDecodeError:
                    self.df_desp = pd.read_csv(path_desp, sep=';', encoding='latin1', dtype=str)

                # Normaliza nomes das colunas 
                # Ex: 'Valor Despesas' vira 'VALOR DESPESAS'
                self.df_desp.columns = [c.strip().upper() for c in self.df_desp.columns]

                # Tenta encontrar a coluna de VALOR dinamicamente
                col_valor = next((c for c in self.df_desp.columns if 'VALOR' in c), None)
                col_cnpj = next((c for c in self.df_desp.columns if 'CNPJ' in c), None)

                if col_valor and col_cnpj:
                    # Renomeia para o padrão interno
                    self.df_desp.rename(columns={col_valor: 'VALOR_PADRAO', col_cnpj: 'CNPJ_PADRAO'}, inplace=True)

                    # LÓGICA DE CONVERSÃO DE NÚMEROS INTELIGENTE
                    def limpar_valor(val):
                        if not val: return 0.0
                        val = str(val).strip()
                        # Se tiver vírgula, assume formato BR (1.000,00) -> 1000.00
                        if ',' in val:
                            val = val.replace('.', '').replace(',', '.')
                        # Se não tiver vírgula, assume formato US (292907.23) -> Mantém
                        return float(val)

                    self.df_desp['VALOR_PADRAO'] = self.df_desp['VALOR_PADRAO'].apply(limpar_valor)
                    
                    # Limpeza de CNPJ para Join
                    self.df_desp['CNPJ_CLEAN'] = self.df_desp['CNPJ_PADRAO'].str.replace(r'\D', '', regex=True)
                else:
                    print("❌ ERRO: Colunas 'VALOR' ou 'CNPJ' não encontradas no CSV de despesas.")
                    print(f"Colunas encontradas: {self.df_desp.columns.tolist()}")
            else:
                 print(f"⚠️ AVISO: Arquivo de Despesas não encontrado: {path_desp}")


            # ---------------------------
            # 3. CARGA DE AGREGADOS
            # ---------------------------
            if os.path.exists(path_agg):
                self.df_agg = pd.read_csv(path_agg, sep=';', encoding='utf-8')
                self.df_agg.columns = [c.strip().upper() for c in self.df_agg.columns]
                
                col_total = next((c for c in self.df_agg.columns if 'TOTAL' in c or 'VALOR' in c), None)
                if col_total:
                     # Garante float
                    def limpar_agg(val):
                        if pd.isna(val): return 0.0
                        if isinstance(val, (int, float)): return float(val)
                        val = str(val).strip()
                        if ',' in val: return float(val.replace(',', '.'))
                        return float(val)
                        
                    self.df_agg[col_total] = self.df_agg[col_total].apply(limpar_agg)
                    self.df_agg.rename(columns={col_total: 'DESPESA_TOTAL'}, inplace=True)

            print("✅ Dados carregados e normalizados com sucesso!")

        except Exception as e:
            print(f"❌ ERRO CRÍTICO NO DATASERVICE: {e}")
            import traceback
            traceback.print_exc()

    def get_operadoras(self, page: int, limit: int, search: str = None):
        resultado = self.df_ops.copy()
        
        col_razao = next((c for c in resultado.columns if 'RAZAO' in c), 'RAZAOSOCIAL')
        col_reg = next((c for c in resultado.columns if 'REGISTRO' in c), 'REGISTROANS')
        
        # Garante que as colunas existam antes de filtrar
        if col_razao not in resultado.columns: resultado[col_razao] = "N/I"
        if col_reg not in resultado.columns: resultado[col_reg] = "000000"

        if search:
            s = search.upper()
            resultado = resultado[
                resultado[col_razao].str.contains(s, na=False) |
                resultado[col_reg].str.contains(s, na=False)
            ]
        
        total = len(resultado)
        inicio = (page - 1) * limit
        fim = inicio + limit
        
        retorno = []
        for _, row in resultado.iloc[inicio:fim].iterrows():
            retorno.append({
                "RegistroANS": row.get(col_reg, ''),
                "CNPJ": row.get('CNPJ', ''),
                "RazaoSocial": row.get(col_razao, ''),
                "UF": row.get('UF', ''),
                "Modalidade": row.get('MODALIDADE', '')
            })

        return {
            "data": retorno,
            "total": total
        }

    def get_operadora_by_registro(self, registro: str):
        col_reg = next((c for c in self.df_ops.columns if 'REGISTRO' in c), 'REGISTROANS')
        
        op = self.df_ops[self.df_ops[col_reg] == registro]
        if op.empty:
            return None
            
        row = op.iloc[0]
        col_razao = next((c for c in self.df_ops.columns if 'RAZAO' in c), 'RAZAOSOCIAL')
        
        return {
            "RegistroANS": row.get(col_reg, ''),
            "CNPJ": row.get('CNPJ', ''),
            "RazaoSocial": row.get(col_razao, ''),
            "UF": row.get('UF', ''),
            "Modalidade": row.get('MODALIDADE', '')
        }

    def get_despesas_by_registro(self, registro: str):
        op_data = self.get_operadora_by_registro(registro)
        if not op_data:
            return None
        
        # CNPJ limpo para comparação
        cnpj_alvo = str(op_data['CNPJ']).replace('.', '').replace('/', '').replace('-', '')
        
        if 'CNPJ_CLEAN' not in self.df_desp.columns:
            return []

        despesas = self.df_desp[self.df_desp['CNPJ_CLEAN'] == cnpj_alvo]
        
        # Mapeamento dinâmico das colunas do seu CSV
        col_data = next((c for c in self.df_desp.columns if 'DATA' in c), None) # Pode não existir no consolidado se for por trim
        col_ano = next((c for c in self.df_desp.columns if 'ANO' in c), 'ANO')
        col_trim = next((c for c in self.df_desp.columns if 'TRIM' in c), 'TRIMESTRE')

        saida = []
        for _, row in despesas.iterrows():
            data_evento = row.get(col_data, f"{row.get(col_trim)}º Tri/{row.get(col_ano)}")
            
            saida.append({
                "Data_Evento": data_evento,
                "Ano": row.get(col_ano, ''),
                "Trimestre": row.get(col_trim, ''),
                "Valor_Despesa": row.get('VALOR_PADRAO', 0.0)
            })
            
        return saida

    def get_dashboard_stats(self):
        if self.df_agg.empty:
            return None
            
        # Garante que UF existe, senão agrupa pelo que der
        grp_col = 'UF' if 'UF' in self.df_agg.columns else self.df_agg.columns[0]
        
        top_uf = (
            self.df_agg.groupby(grp_col)['DESPESA_TOTAL']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        
        retorno = []
        for _, row in top_uf.iterrows():
            retorno.append({
                "UF": row[grp_col],
                "Despesa_Total": row['DESPESA_TOTAL']
            })

        return {"top_estados": retorno}


data_service = DataService()