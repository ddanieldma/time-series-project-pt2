# Conclusão de comparação dos modelos

### Série HOBBIES (Gabrielle)

Para o modelo linear, usou-se uma regressão regularizada. Os hiperparâmetros de regularização ($\alpha$ e l1_ratio) foram escolhidos rigorosamente fora da validação, utilizando validação cruzada temporal (TimeSeriesSplit de 5 folds) restrita ao conjunto de treino. Inicialmente, eu imaginei que a esetratégia recursiva pudesse ser melhor, já que imaginei que lags curtos pudessem influenciar o preço de um dia, mas por segurança testei o direto também e ele acabou performando melhor, provavelmente a regularização não bastou para impedir o erro acumulado das previsões passadas também usadas como input do modelo recursivo.

- Média: 

MAE 110,99 | RMSE 141,31 | MASE 1,216  

- Naive sazonal: 

MAE 102,25 | RMSE 146,65 | MASE 1,120  

- Linear Recursivo (DESCARTADO):

MAE 81,01 | RMSE 101,58 | MASE 0,887

- SARIMA: 

MAE 78,47 | RMSE 95,08 | MASE 0,859

- Linear Direto (escolhido como o modelo linear): 

MAE 78.01 | RMSE 91.42 | MASE 0.854

O linear de estratégia recursiva ultrapassou o de média e naive sazonal, ficando um pouco atrás do SARIMA da task1. O linear de estratégia direta ultrapassou todos e ficou com as melhores métricas. O único motivo de se escolher o direto foi a melhor performance. Os seus melhores hiperparâmetro de regressão foram: alpha=0.01, l1_ratio=1.0, mostrando que ficou a Lasso pura. 

O motivo da escolha de usar regularização no modelo direto é que usei vários lags: lag_28, lag_35, lag_42, ..., que costumam ser correlacionados (a Ridge melhora isso), e talvez defasagens muito distantes (como lag_49 ou lag_56) sejam apenas ruído, bem como tem covariáveis pouco úteis (que são descartadas pela Lasso), como possivelmente o snap_CA que por lógica não afeta os valores da série de hobbies por ser relacionado com comida. Além, claro, de minimizar o overfitting.

