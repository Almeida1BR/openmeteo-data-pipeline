# Open-Meteo Data Pipeline

Projeto guiado de engenharia de dados para coletar dados meteorológicos horários da [Open-Meteo](https://open-meteo.com/), publicá-los em um fluxo Kafka, orquestrar as etapas com Apache Airflow, armazenar o histórico e apresentá-lo em um dashboard próprio.

> **Status:** estrutura inicial em desenvolvimento. As etapas e componentes serão implementados gradualmente como parte do aprendizado de Python e engenharia de dados.

## Objetivos de aprendizagem

- Consumir uma API REST com Python e tratar respostas e falhas.
- Construir um fluxo de ingestão e processamento que possa ser repetido com segurança.
- Aprender conceitos de eventos, produtores e consumidores usando Kafka.
- Agendar e acompanhar execuções com Airflow.
- Armazenar e consultar uma série histórica de dados meteorológicos.
- Construir um dashboard interativo para explorar temperatura e histórico.
- Executar os serviços locais com Docker Compose.

## Arquitetura planejada

```text
Open-Meteo API -> Python extractor -> Kafka -> consumer / storage -> dashboard
                                      ^
                                      |
                           Airflow agenda a coleta
```

Os componentes serão introduzidos por fases. A frequência planejada de coleta é horária. O horário da consulta será registrado separadamente do horário ao qual cada dado retornado se refere, pois previsão e atualização do modelo não significam necessariamente uma observação nova no instante da execução.

## Tecnologias planejadas

- Python para ingestão, transformações, integração com Kafka e dashboard.
- Open-Meteo Forecast API como fonte meteorológica.
- Apache Kafka para transporte de eventos.
- Apache Airflow para agendamento e acompanhamento do pipeline.
- PostgreSQL para persistência do histórico e metadados do Airflow.
- Streamlit para o dashboard.
- Docker Compose para executar os serviços locais.
- pgAdmin para administrar o PostgreSQL e Portainer para acompanhar os containers.

## Pré-requisitos

- Git
- Python 3.14 para o ambiente local do projeto
- Docker Engine e Docker Compose plugin

Airflow será executado no container oficial, separado do ambiente virtual local. Consulte a documentação oficial para requisitos e orientações de execução local antes de iniciar os serviços.

## Ambiente Python local

Ative o ambiente virtual na raiz do repositório:

```bash
source .venv/bin/activate
```

As dependências locais do pipeline e do dashboard serão registradas em `requirements.txt`. As dependências específicas do Airflow ficam isoladas na imagem/container do Airflow.

## Execução com Docker Compose

O Compose reúne Kafka, PostgreSQL, Airflow, dashboard, pgAdmin e Portainer. Antes de iniciar, crie um arquivo `.env` a partir do `.env.example` e substitua as senhas de desenvolvimento.

```bash
docker compose config
docker compose up airflow-init
docker compose up -d
```

Interfaces locais:

- Airflow: http://localhost:8080
- Dashboard: http://localhost:8501
- pgAdmin: http://localhost:5050
- Portainer: https://localhost:9443 (ou http://localhost:9000)

Este ambiente é destinado a desenvolvimento local. As credenciais padrão devem ser trocadas no `.env` antes do primeiro uso; não publique esse arquivo. PostgreSQL usa a versão estável mais recente explicitamente fixada no Compose; as demais imagens estão configuradas com a tag `latest` e podem mudar quando forem atualizadas pelos mantenedores.

## Estrutura do repositório

```text
src/openmeteo_pipeline/  Código Python de ingestão, streaming, storage e transformação
src/dashboard/           Aplicação Streamlit
dags/                    DAGs do Airflow
docker/                  Arquivos de imagem e notas dos serviços
config/                  Configurações não secretas
docs/                    Arquitetura, dicionário de dados e registro de aprendizagem
tests/                   Testes unitários e de integração
data/                    Espaço local para dados brutos e processados (ignorado pelo Git)
```

## Fonte e atribuição

Os dados serão obtidos da Open-Meteo. Antes de publicar ou redistribuir dados, vamos confirmar os termos aplicáveis e incluir a atribuição exigida pela licença da fonte. Cada etapa de ingestão deverá preservar a origem, o horário de coleta e o período de validade do dado.

## Aprendizado guiado

O código será construído passo a passo. Cada etapa terá uma explicação do objetivo, das decisões e dos trechos que você deverá implementar; este repositório não pretende começar com uma solução completa pronta.
