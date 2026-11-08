from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
import pandas as pd

from .load_data_st import carregar_dados
from .prepare_data_st import get_all_data, calcular_estatisticas_treino
from .config_store_total import SERIE, val_dates
from .models_utils import calcular_metricas, save_outputs


def predict_model(X_val_h, stats, model):
    z_hat = model.predict(X_val_h[cols].to_numpy())
    y_hat = pd.Series(
        z_hat * stats["y_std"] + stats["y_mean"],
        index=X_val_h.index,
        name="yhat",
    )
    
    return y_hat

# --- Model setup ------------------------------------------------------
TREE_PARAMS = {
    "max_depth": 8, 
    "min_samples_leaf": 20, 
    "random_state": 0
}

tree_model = DecisionTreeRegressor(**TREE_PARAMS) # type: ignore

# --- Data steps -------------------------------------------------------
train_df, _, cov_df = carregar_dados()
stats = calcular_estatisticas_treino(train_df, cov_df)
X_train_h, y_train_h, X_val_h, y_true = get_all_data()
y_train_naive = train_df[SERIE].to_numpy()

cols = [c for c in X_train_h.columns if c not in ("date", "index")]

# --- Fit and Predict --------------------------------------------------
model_name = 'arvore'
print(f"--- Training {model_name} ---")
    
# 5) Fit
tree_model.fit(X_train_h[cols].to_numpy(), y_train_h.to_numpy())

# 6) Previsão na validação (despadroniza)
y_hat = predict_model(X_val_h, stats, tree_model)

# --- Report -----------------------------------------------------------

# 7) Métricas
validation_metrics = calcular_metricas(
    y_true, 
    y_hat.to_numpy(), 
    y_train_naive
)

# 8) Salvar resultados (assumindo que save_outputs recebe o nome do modelo 
# ou que você adapta para salvar em tabelas diferentes)
save_outputs(y_hat, val_dates, validation_metrics, model_name=model_name)
print(validation_metrics)