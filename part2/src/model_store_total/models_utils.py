import pandas as pd
import numpy as np

from .config_store_total import SERIE, OUTPUT_DIR
from typing import Dict


# --- Functions --------------------------------------------------------
def fit_and_predict(model, X_train_df, y_train_std, X_validation):
    """
    Universal function for fitting and predicting with a model
    """

    # Exclude the date index/column if it's still present
    cols = [c for c in X_train_df.columns if c not in ("date", "index")]
    
    X_train = X_train_df[cols].to_numpy()
    y_train = y_train_std.to_numpy()
    X_val   = X_validation[cols].to_numpy()
    
    model.fit(X_train, y_train)
    return model.predict(X_val)

def calcular_metricas(y_true: np.ndarray, yhat: np.ndarray, y_train_raw: np.ndarray) -> Dict[str, float]:
    """Cálculo das métricas padronizado pela Task 2."""
    err = yhat - y_true
    mae = float(np.abs(err).mean())
    rmse = float(np.sqrt((err**2).mean()))
    mase_scale = float(np.abs(y_train_raw[7:] - y_train_raw[:-7]).mean())
    mase = mae / mase_scale if mase_scale > 0 else float("nan")
    return {"mae": mae, "rmse": rmse, "mase": mase}

def save_outputs(
    y_hat: pd.Series,
    val_dates: pd.DatetimeIndex,
    metrics: Dict[str, float],
    model_name: str
):
    predictions_path = OUTPUT_DIR / f'previsoes_{model_name}_store_total.csv'
    metrics_path = OUTPUT_DIR / f'metricas_{model_name}_store_total.csv'
    
    pd.DataFrame({
        "date": val_dates.strftime("%Y-%m-%d"), "series": SERIE, "modelo": "linear", "yhat": y_hat
    }).to_csv(predictions_path, index=False)
    
    pd.DataFrame([{
        "series": SERIE, "modelo": "linear", "mae": metrics['mae'], "rmse": metrics['rmse'], "mase": metrics['mase']
    }]).to_csv(metrics_path, index=False)