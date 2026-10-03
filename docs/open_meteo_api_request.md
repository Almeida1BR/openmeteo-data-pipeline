# Requisição inicial à Open-Meteo

## Endpoint

```text
https://api.open-meteo.com/v1/forecast?latitude=-19.4658&longitude=-44.2467&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m&timezone=America/Sao_Paulo&forecast_days=1
```

[Abrir esta requisição no navegador](https://api.open-meteo.com/v1/forecast?latitude=-19.4658&longitude=-44.2467&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m&timezone=America/Sao_Paulo&forecast_days=1)

O endereço foi copiado da opção **Chart & URL → API URL** no construtor da documentação da Open-Meteo. A página do construtor, com as opções selecionadas, está [aqui](https://open-meteo.com/en/docs?latitude=-19.4658&longitude=-44.2467&bounding_box=-90,-180,90,180&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m&timezone=America%2FSao_Paulo&forecast_days=1).

## Parâmetros escolhidos

- `latitude=-19.4658` e `longitude=-44.2467`: coordenadas configuradas no navegador para Sete Lagoas.
- `hourly=temperature_2m,relative_humidity_2m`: temperatura a 2 metros e umidade relativa horária.
- `hourly=precipitation_probability,precipitation,weather_code,wind_speed_10m`: probabilidade de precipitação, precipitação total, código meteorológico WMO e velocidade do vento a 10 m.
- `timezone=America/Sao_Paulo`: faz os horários da resposta corresponderem ao fuso local.
- `forecast_days=1`: limita cada consulta a um dia de previsão para o primeiro exercício.

A página de documentação aberta contém seis variáveis horárias: temperatura, umidade relativa, probabilidade de precipitação, precipitação, código meteorológico e velocidade do vento. Ajustei o fuso para São Paulo e limitei o horizonte a um dia para este primeiro experimento. A API Forecast é pública e não exige chave de API.

## Conferência da resposta

A URL foi consultada em 2026-10-03. A resposta deve conter 24 horários e os campos `temperature_2m` (`°C`), `relative_humidity_2m` (`%`), `precipitation_probability` (`%`), `precipitation` (`mm`), `weather_code` (código WMO) e `wind_speed_10m` (`km/h` por padrão), além do fuso `America/Sao_Paulo` e das coordenadas do ponto de grade usado pelo modelo. A localização de grade retornada pode diferir ligeiramente das coordenadas solicitadas.

Este endpoint retorna **previsão horária**, não uma medição observada nova a cada hora. No pipeline, vamos preservar o horário de cada previsão e a hora em que coletamos a resposta. Ao coletar previsões repetidamente, o mesmo horário futuro pode aparecer em várias execuções; isso permitirá estudar atualizações e deduplicação.
