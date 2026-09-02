import streamlit as st
import joblib
import pandas as pd


artifact = joblib.load("models/random_forest_model.pkl")

model = artifact["model"]
features = artifact["features"]
threshold = artifact["threshold"]

st.title("Sistema Industrial de Detecção de Falhas")

st.write(
    "Informe os parâmetros operacionais da máquina para estimar "
    "a probabilidade de ocorrência de falha."
)


st.subheader("Parâmetros da máquina")

air_temperature = st.number_input(
    "Temperatura do ar [K]",
    min_value=250.0,
    max_value=350.0,
    value=300.0
)

process_temperature = st.number_input(
    "Temperatura do processo [K]",
    min_value=250.0,
    max_value=400.0,
    value=310.0
)

rotational_speed = st.number_input(
    "Velocidade de rotação [rpm]",
    min_value=0,
    max_value=3000,
    value=1500
)

torque = st.number_input(
    "Torque [Nm]",
    min_value=0.0,
    max_value=100.0,
    value=40.0
)

tool_wear = st.number_input(
    "Desgaste da ferramenta [min]",
    min_value=0,
    max_value=300,
    value=100
)


input_data = pd.DataFrame(
    [[
        air_temperature,
        process_temperature,
        rotational_speed,
        torque,
        tool_wear
    ]],
    columns=features
)

if st.button("Analisar máquina"):

    probability = model.predict_proba(input_data)[0][1]

    prediction = probability >= threshold

    st.subheader("Resultado da análise")

    st.metric(
        "Probabilidade de falha",
        f"{probability:.2%}"
    )

    if prediction:
        st.error("ALERTA: possível falha detectada.")
    else:
        st.success("Máquina operando normalmente.")