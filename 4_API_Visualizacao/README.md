# Teste 4: API Restful e Dashboard Web

Este módulo final integra o processamento de dados realizado nos testes anteriores em uma aplicação **Full Stack**. O objetivo é disponibilizar os dados através de uma API moderna e visualizá-los em um Dashboard interativo, focado em performance e experiência do usuário (UX).

## 📋 Funcionalidades Implementadas

1.  **Backend (API):** Servidor desenvolvido em **FastAPI** que expõe os dados de operadoras e despesas processados nos testes 1 e 2. Inclui documentação automática (Swagger).
2.  **Frontend (SPA):** Interface reativa desenvolvida em **Vue.js 3** (via CDN) para consulta, listagem paginada e visualização gráfica.
3.  **Arquitetura em Camadas:** O backend foi estruturado utilizando o *Service Pattern*, separando a camada de rotas (HTTP) da camada de dados (Pandas/CSV).

---

## ⚖️ Decisões Técnicas e Trade-offs (Análise Crítica)

Conforme solicitado nos requisitos do teste (Itens 4.2 e 4.3 do PDF), abaixo estão as justificativas para as escolhas de arquitetura.

### 🔌 Backend (Item 4.2)

#### 4.2.1. Escolha do Framework
* **Opção Escolhida:** **FastAPI** (vs Flask).
* **Justificativa:**
    * **Documentação Nativa:** O FastAPI gera automaticamente a documentação interativa (Swagger UI em `/docs`), eliminando a necessidade de manter coleções Postman manuais desatualizadas.
    * **Performance e Tipagem:** O uso de *Type Hints* (Pydantic) garante validação rigorosa de dados na entrada e saída. Além disso, o suporte nativo a `async/await` oferece melhor performance para operações de I/O futuras.

#### 4.2.2. Estratégia de Paginação
* **Opção Escolhida:** **Offset-based** (Página 1, Página 2...).
* **Justificativa:**
    * **UX Administrativa:** Para tabelas de consulta onde o usuário precisa saber o total de registros ou "saltar" para uma página específica, o Offset é mais intuitivo que o *Cursor-based* (que é melhor para feeds infinitos).
    * **Volume de Dados:** Como estamos lidando com DataFrames em memória, o custo computacional do *slicing* é irrelevante para o volume atual.

#### 4.2.3. Cache vs Queries Diretas
* **Opção Escolhida:** **Pré-carga em Memória (In-Memory Database)**.
* **Justificativa:**
    * **Natureza dos Dados:** Os dados vêm de arquivos CSV estáticos gerados nos testes anteriores.
    * **Estratégia:** Ao carregar os CSVs para a memória RAM (Pandas DataFrame) na inicialização da API, eliminamos a latência de disco/banco. Isso torna a resposta da rota `/api/estatisticas` instantânea, dispensando a complexidade de um Redis externo para este escopo.

---

### 💻 Frontend (Item 4.3)

#### 4.3.1. Estratégia de Busca/Filtro
* **Opção Escolhida:** **Busca no Servidor** (Server-side Search).
* **Justificativa:**
    * **Escalabilidade:** Filtrar no cliente (*Client-side*) exigiria baixar a lista completa de operadoras para o navegador. Se a base crescer para 100.000 registros, a aplicação travaria o navegador do usuário. A busca no servidor é a única solução escalável profissionalmente.

#### 4.3.2. Gerenciamento de Estado
* **Opção Escolhida:** **Reactivity API (`ref`/`reactive`)** (vs Vuex/Pinia).
* **Justificativa:**
    * **Complexidade vs Necessidade:** A aplicação possui baixo nível de compartilhamento de estado global. Introduzir uma biblioteca de Store (Pinia) adicionaria *boilerplate* desnecessário. O uso de variáveis reativas locais com a Composition API é mais limpo, moderno e suficiente para manter o estado da tabela e dos modais.

#### 4.3.4. Tratamento de Erros e Loading
* **Estratégia:** Feedback Visual Específico.
* **Justificativa:**
    * **UX (Experiência do Usuário):** Diferenciamos visualmente os estados para não confundir o usuário:
        * **Loading:** Mensagem ou Spinner durante a requisição.
        * **Empty State:** Mensagem "Nenhum registro encontrado" quando a busca é válida mas sem retorno.
        * **Erro:** Status visual "Offline 🔴" e logs no console em caso de falha de conexão, permitindo que a interface degrade graciosamente sem travar.

---

## 🚀 Como Executar

A solução foi projetada para rodar de forma leve, sem necessidade de *build steps* de frontend.

### 1. Iniciar o Backend
```bash
cd 4_API_Visualizacao/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
    * **API:** `http://127.0.0.1:8000`
    * **Documentação (Swagger):** `http://127.0.0.1:8000/docs`

2.  **Inicie o Frontend:**
    Basta abrir o arquivo `4_API_Visualizacao/frontend/index.html` diretamente no seu navegador (Chrome, Edge ou Firefox).
    * *A aplicação se conectará automaticamente à API local.*

---

## 📂 Estrutura do Módulo

Utilizamos o padrão **Service Layer** no backend para desacoplar a lógica de rotas da lógica de manipulação de dados, facilitando manutenção e testes.

```text
4_API_Visualizacao/
│
├── backend/                 # Servidor Python
│   ├── main.py              # Configuração do App e CORS
│   ├── routes.py            # Definição dos Endpoints (Controller)
│   ├── service.py           # Regras de Negócio e Leitura de CSV (Service)
│   └── requirements.txt     # Dependências (FastAPI, Pandas)
│
├── frontend/                # Cliente Web
│   └── index.html           # Single File Application (Vue.js + Tailwind)
│
└── README.md                # Documentação técnica
```

## 👤 Autor: Ítallo de Santana Guimarães