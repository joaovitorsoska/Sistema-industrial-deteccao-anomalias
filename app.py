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

col1, col2 = st.columns(2)

with col1:
    air_temperature = st.number_input(
        "Temperatura do ar [K]",
        min_value=250.0,
        max_value=350.0,
        value=300.0
    )

    rotational_speed = st.number_input(
        "Velocidade de rotação [rpm]",
        min_value=0,
        max_value=3000,
        value=1500
    )

    tool_wear = st.number_input(
        "Desgaste da ferramenta [min]",
        min_value=0,
        max_value=300,
        value=100
    )

with col2:
    process_temperature = st.number_input(
        "Temperatura do processo [K]",
        min_value=250.0,
        max_value=400.0,
        value=310.0
    )

    torque = st.number_input(
        "Torque [Nm]",
        min_value=0.0,
        max_value=100.0,
        value=40.0
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



st.progress(float(probability))

if prediction:
    st.error(
        f"ALERTA: possível falha detectada.\n\n"
        f"A probabilidade estimada é de {probability:.2%}, "
        f"acima do threshold de {threshold:.0%}."
    )
else:
    st.success(
        f"Máquina operando normalmente.\n\n"
        f"A probabilidade estimada de falha é de {probability:.2%}, "
        f"abaixo do threshold de {threshold:.0%}."
    )