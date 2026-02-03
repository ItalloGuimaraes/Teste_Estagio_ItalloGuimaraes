# Teste 2: Validação, Enriquecimento e Análise Estatística

Este módulo é responsável por processar os dados brutos consolidados no Teste 1, aplicando regras de negócio, validação matemática de documentos e enriquecimento com dados cadastrais externos.

## 📋 Funcionalidades Implementadas

1.  **Validação de Dados:** Verifica a integridade dos CNPJs utilizando cálculo de dígitos verificadores (Módulo 11).
2.  **Enriquecimento (Data Enrichment):** Cruza os dados financeiros com a base cadastral oficial da ANS (CADOP) para adicionar `Registro ANS`, `Modalidade` e `UF`.
3.  **Agregação Estatística:** Calcula métricas financeiras (Soma, Média e Desvio Padrão) agrupadas por Operadora e Estado.

---

## ⚖️ Decisões Técnicas e Trade-offs (Análise Crítica)

Conforme solicitado no desafio, abaixo estão as justificativas para as estratégias adotadas no tratamento dos dados.

### 1. Tratamento de CNPJs Inválidos
**Cenário:** O dataset contém registros onde o CNPJ não satisfaz a validação matemática (dígitos verificadores incorretos).
* **Estratégia Escolhida:** *Flagging* (Marcação). Criamos uma coluna booleana `CNPJ_Valido` em vez de descartar o registro.
* **Justificativa:**
    * **Integridade Contábil:** Em um relatório financeiro, remover uma linha invalida o saldo total. Se uma operadora reportou R$ 1 milhão mas errou o CNPJ, esse dinheiro ainda existe contabilmente.
    * **Rastreabilidade:** Marcar o dado permite que uma equipe de auditoria filtre e corrija a origem do erro posteriormente.

### 2. Estratégia de Join (Enriquecimento)
**Cenário:** Existem CNPJs no arquivo de despesas que não foram encontrados no arquivo atual de operadoras ativas (CADOP).
* **Estratégia Escolhida:** `Left Join` (Manter todas as despesas).
* **Justificativa:**
    * **Prioridade do Dado Financeiro:** O objetivo principal é analisar despesas. Operadoras podem ter sido desativadas ou mudado de registro, mas suas despesas históricas devem constar no relatório.
    * **Tratamento de Falhas:** Registros sem correspondência no cadastro são preenchidos com `UF = "N/I"` (Não Informado) e `Modalidade = "Desconhecida"`, garantindo que o pipeline não quebre.

### 3. Agregação e Performance
**Cenário:** Calcular Média e Desvio Padrão de milhares de registros.
* **Estratégia Escolhida:** Processamento em Memória (`Pandas`).
* **Justificativa:**
    * **Volume de Dados:** O volume processado (centenas de MBs) cabe confortavelmente na memória RAM de computadores modernos. O uso de frameworks distribuídos (como Spark) seria um *overkill* (complexidade desnecessária) para este volume.
    * **Ordenação:** A ordenação final é feita pelo `Valor Total de Despesas` (decrescente), focando a visualização nos maiores "players" do mercado.

---

## 🚀 Como Executar

Este módulo foi projetado para ser **modular**. Ele busca automaticamente os dados gerados pelo Teste 1.

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute:**
    ```bash
    python main.py
    ```
    *O script irá buscar `consolidado_despesas.csv` (ou .zip) na pasta do Teste 1, validar os dados, baixar o CADOP atualizado e gerar o relatório final.*

3.  **Resultado:**
    O arquivo `despesas_agregadas.csv` será gerado na raiz da pasta.

---

## 📂 Estrutura do Módulo

A solução foi arquitetada utilizando o padrão de **Separação de Responsabilidades (SoC)**, onde cada script dentro de `src/` possui uma função única e isolada.

```text
2_Transformacao_Validacao/
│
├── main.py                  # Ponto de entrada (Orquestrador do Pipeline)
├── requirements.txt         # Lista de bibliotecas (Pandas, Requests)
├── README.md                # Documentação técnica e justificativas
├── despesas_agregadas.csv   # (Output) Relatório Final Gerado
│
├── src/                     # Código Fonte Modularizado
│   ├── validator.py         # Lógica de validação matemática de CNPJ
│   ├── enricher.py          # Lógica de download e Join com CADOP
│   └── aggregator.py        # Lógica de estatística e agrupamento
│
└── data/                    # Diretório de entrada (Input)
    └── .gitkeep             # Garante a existência da pasta no repositório
```

## 👤 Autor: Ítallo de Santana Guimarães