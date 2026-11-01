from pathlib import Path
import pandas as pd

datos = Path("./dados")

treino = pd.read_csv(
    datos / "treino.csv",
    parse_dates=["date"],
)[["date", "FOODS"]]

covariaveis = pd.read_csv(
    datos / "covariaveis.csv",
    parse_dates=["date"],
)[[
    "date",
    "snap_CA",
    "event_name_1",
    "event_type_1",
    "event_name_2",
    "event_type_2",
    "preco_FOODS",
]]

base_treino = treino.merge(
    covariaveis,
    on="date",
    how="left",
    validate="one_to_one",
)

columnas_eventos = [
    "event_name_1", "event_type_1",
    "event_name_2", "event_type_2",
]

base_treino[columnas_eventos] = (
    base_treino[columnas_eventos].fillna("sem_evento")
)

print(base_treino.head())