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

### Séria store_total (Daniel)

Para fazer a regressão linear da série store_total, parti do seguinte pressuposto: como essa série agrega FOODS e HOBBIES, ela tem magnitude maior e, no agregado, menos ruído relativo do que as categorias individuais; por isso, um modelo parcimonioso — com poucas covariáveis bem escolhidas — tende a generalizar melhor do que um modelo com muitas features correlacionadas, que só aumentariam a variância sem ganho de sinal.

Para tanto, optei por um conjunto enxuto de covariáveis conhecidas na origem (2016-03-27): dummies de dia da semana (segunda como referência), snap_CA, flag geral de evento e dummies por tipo de evento (Cultural, National, Religious, Sporting), e o preço da semana padronizado (preco_store_total). Adicionei um lag de 28: na estratégia direta, ele é o menor lag disponível para todo o horizonte h = 1..28, e ancora o nível recente no mesmo dia da semana de quatro semanas antes. Lags curtos (lag-7, lag-1) não existem para todo o horizonte na direta; e lag-364 (um ano) descartaria ~19% do treino e ancoraria no nível de um ano atrás, menos relevante para 28 dias. A recursividade foi evitada justamente para não escalar erro de previsão ao longo dos 28 passos. Por fim, adicionei os dummies de dia da semana para modelar o padrão semanal de vendas em cada dia específico, que o lag-28 sozinho não cobre em todos os passos.

Com isso, temos cerca de 13 covariáveis para ~1.856 pontos de dados no treino (após descartar as 28 primeiras linhas sem lag), razão de ~140 pontos por covariável. Nesse regime, o OLS já tem variância baixa e dispensa regularização.

**Comparação com baselines**

| Modelo | MAE | RMSE | MASE |
|--------|-----|------|------|
| naive_sazonal | 459,18 | 655,47 | 1,056 |
| sarima | 271,76 | 359,02 | 0,625 |
| linear | 198,89 | 271,09 | 0,457 |

Contra o naive_sazonal: o linear vence nas três métricas. MAE cai 56,7% (459,18 → 198,89), RMSE cai 58,6% (655,47 → 271,09) e o MASE vai de 1,056 para 0,457 — abaixo de 1, o que significa que o modelo bate a escala do naive sazonal semanal in-sample do treino, a mesma escala usada na Task 1.

Contra o sarima da Task 1 (mesma ordem, ajuste até 2016-03-27): o linear também vence. MAE 26,8% menor (271,76 → 198,89), RMSE 24,5% menor (359,02 → 271,09) e MASE de 0,625 para 0,457.

Em store_total, portanto, o linear não perde para o naive sazonal nem para o SARIMA em nenhuma das três métricas, e não há ressalva a registrar para esta série nesse quesito. O ganho sobre o naive sazonal é o esperado conceitualmente: o naive repete a última semana do treino sem ajustar por SNAP, evento, preço ou nível do lag-28; o linear faz exatamente esse ajuste, mantendo a mesma estrutura direta (sem recursão) e sem usar o y da validação em nenhuma coluna.

