import pandas as pd
import streamlit as st
import plotly.express as px

from openmeteo_pipeline.storage.repository import get_latest_weather_forecast

st.set_page_config(page_title="OpenMeteo - Sete Lagoas", layout="wide")
st.title("Previsão do tempo - Sete Lagoas")

records = get_latest_weather_forecast()

if not records:
    st.info("Ainda não há previsões disoníveis no banco de dados.")
else:
    weather_df = pd.DataFrame(records)
    st.dataframe(weather_df, use_container_width=True)

    first_forecast = weather_df.iloc[0]

    temperature_col, humidity_col, rain_col = st.columns(3)

    temperature_col.metric(
        "Temperatura",
        f"{first_forecast['temperature_2m']:.1f} ºC"
    )

    humidity_col.metric(
        "Umidade relativa",
        f"{first_forecast['relative_humidity_2m']}%"
    )
    rain_col.metric(
        "Probabilidade de precipitação",
        f"{first_forecast['precipitation_probability']}%"
    )

    temperature_chart = px.line(

        weather_df,
        x="forecast_time",
        y="temperature_2m",
        markers=True,
        title="Temperatura prevista por hora",
        labels={
            "forecast_time": "Horário",
            "temperatura_2m": "Temperatura (ºC)"
        }
    )
    st.plotly_chart(temperature_chart, use_container_width=True)