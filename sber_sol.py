import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot
import statsmodels.api as sm
import itertools
import warnings


dt=pd.read_csv('C:/bank.csv')

dt.drop('value_usd', axis=1, inplace=True)
dt = dt[(dt['bank_group_id']==1) & (dt['sector_id']<5)]
dt.drop(['sector_id', 'bank_group_id'], axis = 1, inplace = True)
dt['report_date'] = pd.to_datetime(dt['report_date'], format = '%Y-%m-%d')
dt = dt.set_index(pd.DatetimeIndex(dt['report_date'])) 
dt.drop(['report_date'], axis = 1, inplace = True)
print(dt.isna().sum())


dt= dt.groupby([dt.index])['value_rub'].sum()
pyplot.plot(dt)
pyplot.show()

test = sm.tsa.adfuller(dt)   # проверяем стационарность по Фуллеру
print ('p-value: ', test[1])

decomposition = seasonal_decompose(dt, model='additive') 
decomposition.plot()
pyplot.show()

trend_part = decomposition.trend # тренд
seasonal_part = decomposition.seasonal # сезонная составляющаяя
residual_part = decomposition.resid # шум

pyplot.plot(trend_part)
pyplot.show()


# SARIMA подбор коэфицентов
p = d = q = range(0, 2)

pdq = list(itertools.product(p, d, q))

seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

# подбор коэффициентов через AIC
warnings.filterwarnings("ignore") # выключаем предупреждения
for param in pdq:
    for param_seasonal in seasonal_pdq:
       try:
            mod = sm.tsa.statespace.SARIMAX(trend_part,
            order=param,
            seasonal_order=param_seasonal,
            enforce_stationarity=False,
            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
       except:
            continue


# рассчет для оптимальных коэф. (1,1,1)(0,0,1,12) из минимального AIC (795)
mod = sm.tsa.statespace.SARIMAX(trend_part,
order=(1, 1, 1),
seasonal_order=(0, 0, 1, 12),
enforce_stationarity=False,
enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

results.plot_diagnostics(figsize=(15, 12))
plt.show()

pred = results.get_prediction(start=pd.to_datetime('2018-05-01'), dynamic=False) # прогноз ведем с этой даты
pred_ci = pred.conf_int()

ax = trend_part['2008':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
ax.fill_between(pred_ci.index,
pred_ci.iloc[:, 0],
pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('value_rub')
plt.legend()
plt.show()

y_forecasted = pred.predicted_mean
y_truth = trend_part['2018-05-01':] #данные для сравнения 

# Вычисляем MSE и MAPE
mse = ((y_forecasted - y_truth) ** 2).mean()
print('MSE is {}'.format(round(mse, 2)))
mape = np.mean(np.abs((y_truth - y_forecasted) / y_truth)) * 100
print('MAPE is {}'.format(round(mape, 2)))



