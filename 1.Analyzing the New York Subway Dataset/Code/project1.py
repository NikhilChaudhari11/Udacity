# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 07:49:55 2014

@author: Administrator
"""
# Package Laoding
import pandas
import numpy
import scipy
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble.partial_dependence import plot_partial_dependence
from ggplot import *


# Data Laoding
raw_data = pandas.read_csv('turnstile_weather_v2.csv')

# Statistical Test
enter_rain = raw_data[raw_data['rain']==1]['ENTRIESn_hourly']
enter_norain = raw_data[raw_data['rain']==0]['ENTRIESn_hourly']
rain_mean = numpy.mean(enter_rain)
norain_mean = numpy.mean(enter_norain)
rain_median = numpy.median(enter_rain)
norain_median = numpy.median(enter_norain)
(u, pvalue) = scipy.stats.mannwhitneyu(enter_rain,enter_norain)

# Linear Regression
data = pandas.read_csv('turnstile_weather_lag.csv')
model_ols = smf.ols('ENTRIESn_hourly~weekday + fog + rain + hour + precipi + pressurei + tempi + wspdi + meanprecipi + meanpressurei + meantempi + meanwspdi + Lag_1 + Lag_2 + Lag_3 + Lag_4 + Lag_5 + Lag_6', data=data).fit()
model_ols.summary()

# Beyond Linearity
X_train = data[['weekday','fog','rain','hour','precipi','pressurei','tempi','wspdi','meanprecipi','meanpressurei','meantempi','meanpressurei','meantempi','meanwspdi','Lag_1','Lag_2','Lag_3','Lag_4','Lag_5','Lag_6']]
y_train = data['ENTRIESn_hourly']
rf = RandomForestRegressor(n_estimators=10)
model_rf = rf.fit(X_train, y_train)

feature_names = ('weekday','fog','rain','hour','precipi','pressurei','tempi','wspdi','meanprecipi','meanpressurei','meantempi','meanpressurei','meantempi','meanwspdi','Lag_1','Lag_2','Lag_3','Lag_4','Lag_5','Lag_6')
feature_imp = pandas.Series(rf.feature_importances_, index=feature_names)
feature_imp.sort()
feature_imp.plot(kind='barh')

# Visualization
qplot(enter_rain, geom="histogram")
qplot(enter_norain, geom="histogram")




