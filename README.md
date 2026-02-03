# Teste Técnico - Estágio em Desenvolvimento e Dados

Este repositório contém as soluções desenvolvidas por **Ítallo de Santana Guimarães** para o processo seletivo de estágio. O projeto simula um pipeline real de dados, desde a extração (Web Scraping) até a visualização (Dashboard Web), passando por engenharia e análise de dados.

## 📂 Estrutura do Repositório

### [Teste 1: ETL e Web Scraping da ANS](./1_Leitura_Transformacao_Dados)
Solução em **Python** para extração, tratamento e consolidação de dados de despesas das operadoras de planos de saúde.
* **Destaques:** Crawler resiliente para o CADOP, tratamento automático de encoding e log de inconsistências.
* [Ver Documentação Técnica e Como Executar](./1_Leitura_Transformacao_Dados/README.md)

---

### [Teste 2: Validação, Enriquecimento e Estatística](./2_Transformacao_Validacao)
Pipeline de Qualidade de Dados (Data Quality) que aplica regras de negócio e cruza informações financeiras com cadastrais.
* **Destaques:** Validação matemática de CNPJ (Módulo 11), arquitetura modular (`src/`) e cálculo de estatísticas agregadas em memória.
* [Ver Documentação Técnica e Como Executar](./2_Transformacao_Validacao/README.md)

---

### [Teste 3: Banco de Dados e Análise SQL](./3_Banco_de_Dados)
Modelagem e implementação de banco de dados relacional para armazenamento histórico e queries analíticas.
* **Destaques:** Modelagem Híbrida (Normalizada + Dimensional), ETL via `LOAD DATA` (SQL Puro) e uso de Window Functions para análise temporal.
* [Ver Documentação Técnica e Como Executar](./3_Banco_de_Dados/README.md)

---

### [Teste 4: API Restful e Dashboard Web](./4_API_Visualizacao)
Aplicação **Full Stack** para disponibilização e visualização dos dados processados.
* **Destaques:** Backend em **FastAPI** com *Service Pattern*, Frontend reativo em **Vue.js** (SPA) e documentação automática via Swagger.
* [Ver Documentação Técnica e Como Executar](./4_API_Visualizacao/README.md)

---

## 🚀 Guia de Execução (Pipeline Completo)

Para garantir o fluxo correto dos dados, recomenda-se a execução sequencial dos módulos:

1.  **Executar Teste 1:** Gera o arquivo consolidado de despesas.
2.  **Executar Teste 2:** Gera os arquivos de operadoras ativas e agregados estatísticos.
3.  **Executar Teste 3:** Importa os CSVs gerados para o MySQL.
4.  **Executar Teste 4:** Sobe a API que lê os dados gerados e exibe o Dashboard.

## ✅ Testes Automatizados (QA)

Como diferencial de qualidade e robustez, foram implementados testes automatizados cobrindo tanto a lógica de validação quanto a integridade da API.

### 1. Testes Unitários (Lógica de Negócio)
Validação do algoritmo de cálculo de dígitos verificadores de CNPJ.
* **Comando:** `python -m unittest 2_Transformacao_Validacao/tests/test_validator.py`

### 2. Testes de Integração (API Endpoints)
Validação das rotas da API, testando paginação, filtros de busca, tratamento de 404 e estrutura JSON de resposta.
* **Ferramenta:** `FastAPI TestClient` (baseado em `httpx`).
* **Comando:** `cd 4_API_Visualizacao/backend && python -m unittest test_api.py`

## ☁️ Cloud & DevOps (Diferencial)

Para demonstrar a capacidade de **Aplicação de Recursos de Nuvem** e prontidão para produção, o projeto foi totalmente containerizado.

A aplicação é **Cloud Native**, pronta para ser implantada em serviços como **AWS ECS**, **Google Cloud Run** ou **Azure App Service**.

### 🐳 Como rodar com Docker (Simulação de Nuvem)

Se você tiver o Docker instalado, pode subir a arquitetura completa (Frontend + Backend) com um único comando, sem configurar Python localmente:

```bash
docker-compose up --build
```
* **Frontend:** Acessível em `http://localhost:80` (Servido via Nginx)
* **Backend:** Acessível em `http://localhost:8000` (API Python)
* **Volume Mapping:** O container monta automaticamente os diretórios de dados locais para leitura dos CSVs processados.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando uma stack moderna de Engenharia de Dados e Desenvolvimento Web:

* **Linguagem:** Python 3.12+
* **Engenharia de Dados:** Pandas, BeautifulSoup4, Requests
* **Banco de Dados:** MySQL 8.0, SQL (DDL/DML/DQL)
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** Vue.js 3, TailwindCSS, Chart.js
* **Controle de Versão:** Git & GitHub

---
*Projeto desenvolvido em Fevereiro de 2026.*