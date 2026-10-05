# Arquitetura do pipeline

## Fluxo de dados

```text
Airflow (DAG horário)
    └── extrai previsão da Open-Meteo
        └── achata a resposta horária em registros
            └── publica eventos no Kafka: weather.forecast.hourly
                └── consumidor grava no PostgreSQL
                    └── dashboard Streamlit consulta a coleta mais recente
```

O DAG `openmeteo_weather_hourly` agenda a execução no minuto zero de cada hora, no fuso `America/Sao_Paulo`. Ele consulta as coordenadas configuradas para Sete Lagoas (`-19.4658`, `-44.2467`) e publica as previsões horárias retornadas pela API Forecast.

## Componentes e responsabilidades

| Componente | Responsabilidade |
| --- | --- |
| `src/openmeteo_pipeline/ingestion/extract.py` | Faz a requisição HTTP à Open-Meteo e valida o status HTTP. |
| `src/openmeteo_pipeline/transformations/validate.py` | Confere os campos horários requeridos e o alinhamento do tamanho das listas. |
| `src/openmeteo_pipeline/transformations/clean.py` | Converte as listas paralelas da resposta em registros por horário e adiciona `collected_at`. |
| `src/openmeteo_pipeline/streaming/producer.py` | Serializa registros JSON e publica-os no tópico Kafka com chave por local e horário previsto. |
| `src/openmeteo_pipeline/streaming/consumer.py` | Consome eventos, persiste cada registro e confirma o offset após salvar. |
| `src/openmeteo_pipeline/storage/` | Define a conexão, o modelo PostgreSQL e as operações de gravação e consulta. |
| `dags/weather_pipeline.py` | Agenda e coordena extração e publicação, com tentativas em caso de falha. |
| `src/dashboard/app.py` | Lê a coleta mais recente e apresenta tabela, indicadores e gráfico de temperatura. |

## Persistência e repetição

O PostgreSQL guarda previsões de várias coletas. A restrição `uq_weather_forecast_snapshot` identifica um registro por localização, horário previsto e horário de coleta; a gravação ignora duplicatas dessa mesma combinação. Assim, uma nova coleta pode guardar uma revisão da previsão para o mesmo horário futuro sem sobrescrever a coleta anterior.

O consumidor desativa o commit automático. Ele confirma o offset Kafka apenas depois que a gravação no PostgreSQL termina, para que uma falha antes da persistência permita reprocessar a mensagem.

## Consulta usada pelo dashboard

`get_latest_weather_forecast()` seleciona o maior `collected_at` disponível e devolve os registros daquela coleta ordenados por `forecast_time`. Portanto, a tela atual representa a última resposta da API; ela não agrega várias coletas nem mostra o histórico completo. A exploração histórica continua como etapa futura.

## Serviços locais

Docker Compose executa Kafka, PostgreSQL, Airflow, o consumidor, o dashboard, pgAdmin e Portainer. O Airflow e a tabela meteorológica compartilham a instância PostgreSQL local, mas usam tabelas diferentes. O dashboard se conecta ao banco com o driver SQLAlchemy `psycopg` e recebe `PYTHONPATH=/app/src` para importar o pacote do pipeline.

## Limites conhecidos

- A fonte entrega previsão horária, não medições observadas.
- O dashboard inicial está em desenvolvimento; a tela e a consulta precisam de validação integrada com o banco.
- A consulta atual não inclui `relative_humidity_2m` no dicionário de saída, embora a tela tente ler esse campo para um indicador. Corrigir essa diferença antes da primeira execução integrada do dashboard.
- A tabela `weather_forecast` é criada pelo consumidor no início do processo. É necessário que essa inicialização ocorra antes da primeira consulta do dashboard.
- Kafka e PostgreSQL usam volumes nomeados do Compose para manter seus dados entre reinicializações dos containers.
