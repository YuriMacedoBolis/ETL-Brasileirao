# Brasileirao API ETL Pipeline

## Descricao do Projeto
Este repositorio contem um pipeline ETL (Extract, Transform, Load) automatizado, desenvolvido em Python, para a captura, tratamento e analise estruturada de dados do Campeonato Brasileiro de Futebol (Serie A). O projeto consome dados diretamente de uma API REST profissional (API-Football), normaliza estruturas JSON complexas e aninhadas em matrizes tabulares usando a biblioteca Pandas, e realiza analises dedutivas generalistas e especificas por clube.

O objetivo do projeto e demonstrar a aplicacao pratica de boas praticas em engenharia de dados, incluindo o consumo seguro de APIs com autenticacao via headers, manipulacao defensiva de dicionarios para prevencao de falhas, seguranca de credenciais com variaveis de ambiente e modularizacao analitica.

## Funcionalidades
* **Extracao Automatizada (Extract):** Conexao com endpoints HTTP utilizando a biblioteca Requests, com passagem parametrizada de filtros de temporada e identificadores de liga, alem de gerenciamento de autenticacao seguro.
* **Transformacao e Tratamento de Dados (Transform):** Conversao de estruturas JSON massivas e de multiplas camadas em DataFrames do Pandas. A desestruturacao dos dados e feita de forma defensiva utilizando o metodo `.get()`, minimizando a ocorrencia de excecoes do tipo KeyError caso o schema da API sofra alteracoes locais.
* **Enriquecimento Logico:** Criacao de metricas de Business Intelligence (BI) nao nativas da API, como o calculo percentual de aproveitamento de pontos de cada equipe com base nas partidas disputadas.
* **Analise Relacional Integrada (Drill-Down):** Utilizacao de identificadores unicos extraidos na primeira etapa do pipeline para correlacionar e consultar um segundo endpoint analitico de estatisticas individuais por clube, simulando o comportamento de chaves estrangeiras em ecossistemas de dados.
* **Carga de Dados (Load):** Exportacao automatizada da matriz limpa e higienizada para um arquivo no formato CSV, alem da exibicao de logs estruturados de classificacao e estatisticas direto no terminal.

## Stack Tecnologica
* **Python 3.x**
* **Pandas:** Modelagem de dados, tratamento de nulos e calculos vetoriais.
* **Requests:** Comunicacao HTTP e consumo da API REST.
* **Python-dotenv:** Gerenciamento de configuracoes locais e desacoplamento de credenciais.

## Estrutura do Repositorio
* `main.py`: Script principal contendo o fluxo logico do pipeline ETL.
* `requirements.txt`: Declaracao de dependencias necessarias para a replicacao do ambiente de execucao.
* `.env.example`: Modelo de configuracao para as variaveis de ambiente obrigatorias.
* `.gitignore`: Instrucoes de descarte para arquivos locais de dados (CSV) e credenciais protegidas (`.env`).

## Como Executar

1. Certifique-se de possuir o Python instalado em seu ambiente de desenvolvimento.
2. Clone este repositorio e instale as dependencias do projeto atraves do terminal:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo chamado `.env` na raiz do projeto, utilizando como referencia o arquivo `.env.example`, e preencha com a sua respectiva chave de autenticacao:
```text
API_KEY=sua_chave_gerada_na_api
```

4. Execute o pipeline de ingestao e tratamento:
```bash
python main.py
```

## Tratamento de Excecoes e Resiliencia
O pipeline foi projetado para atuar sob condicoes reais de redes distribuidadas. O script valida o status code das respostas HTTP antes de prosseguir para a etapa de parsing e possui checagens condicionais para logs de limites de requisicoes estourados ou chaves invalidas retornadas pela camada de aplicacao do servidor. O uso de blocos try-except garante o isolamento logico em caso de consultas por termos nao localizados na base de dados historicos.
