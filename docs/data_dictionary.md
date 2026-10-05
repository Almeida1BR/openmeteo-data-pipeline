# Dicionário de dados

## Origem e granularidade

Os dados vêm da [Open-Meteo Forecast API](open_meteo_api_request.md), para o ponto configurado em Sete Lagoas. A consulta pede previsão horária de um dia. Cada evento Kafka e cada linha da tabela correspondem a uma variável horária de previsão em uma localização e em uma coleta específica.

## Tabela `weather_forecast`

| Campo | Tipo no PostgreSQL | Nulo? | Significado |
| --- | --- | --- | --- |
| `id` | `INTEGER` | Não | Chave primária interna. |
| `latitude` | `FLOAT` | Não | Latitude do ponto consultado. |
| `longitude` | `FLOAT` | Não | Longitude do ponto consultado. |
| `forecast_time` | `TIMESTAMP WITH TIME ZONE` | Não | Horário ao qual a previsão se refere, interpretado no fuso `America/Sao_Paulo`. |
| `collected_at` | `TIMESTAMP WITH TIME ZONE` | Não | Instante UTC em que a resposta foi convertida em registros. |
| `temperature_2m` | `FLOAT` | Sim | Temperatura do ar a 2 m, em °C. |
| `relative_humidity_2m` | `FLOAT` | Sim | Umidade relativa a 2 m, em %. |
| `precipitation_probability` | `FLOAT` | Sim | Probabilidade de precipitação, em %. |
| `precipitation` | `FLOAT` | Sim | Precipitação prevista, em mm. |
| `weather_code` | `INTEGER` | Sim | Código meteorológico WMO retornado pela API. |
| `wind_speed_10m` | `FLOAT` | Sim | Velocidade do vento a 10 m, em km/h conforme unidade padrão solicitada. |

Valores meteorológicos são anuláveis porque a fonte pode não fornecer um valor para determinado horário. Latitude, longitude e timestamps são obrigatórios para identificar e contextualizar o registro.

## Chave de unicidade

A restrição `uq_weather_forecast_snapshot` combina `latitude`, `longitude`, `forecast_time` e `collected_at`. Uma repetição do mesmo evento da mesma coleta não cria uma linha duplicada. Se uma coleta posterior alterar a previsão de um horário, o novo `collected_at` preserva esse snapshot como outra linha.

## Campos da mensagem Kafka

O produtor publica um objeto JSON no tópico `weather.forecast.hourly`. Cada mensagem inclui `latitude`, `longitude`, os valores horários e `collected_at`. A chave Kafka é formada pela latitude e longitude arredondadas a quatro casas decimais e pelo horário previsto, para identificar o mesmo local e horário entre coletas.

## Dados retornados à tela inicial

A função `get_latest_weather_forecast()` retorna os registros da maior data de coleta e os ordena pelo horário previsto. O dashboard usa `forecast_time` no eixo temporal e os campos meteorológicos para a tabela e os indicadores. No código atual, o dicionário de saída da consulta ainda omite `relative_humidity_2m`, campo lido pelo cartão de umidade da tela; alinhar esses campos antes da execução integrada. A interface ainda não foi validada com dados reais do banco.
