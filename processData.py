import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pylab
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.seasonal import seasonal_decompose


class Carbon:
    def __init__(self, path):

        dateparse = lambda x: pd.to_datetime(x, format='%Y%m', errors = 'coerce')
        df = pd.read_csv(path, parse_dates=['YYYYMM'], index_col='YYYYMM', date_parser=dateparse)

        self.ts = df[pd.Series(pd.to_datetime(df.index, errors='coerce')).notnull().values]
        self.ts['Value'] = pd.to_numeric(self.ts['Value'] , errors='coerce')

        Emissions = self.ts.iloc[:,1:]   # Monthly total emissions (mte)
        Emissions= Emissions.groupby(['Description', pd.TimeGrouper('M')])['Value'].sum().unstack(level = 0)
        self.mte = Emissions['Natural Gas Electric Power Sector CO2 Emissions'] # monthly total emissions (mte)

        

    def getEnergySources(self):
        return self.ts.groupby('Description')

    def getCO2perSource(self):
        return self.ts.groupby('Description')['Value'].sum().sort_values()

    def getMonthlyGreenGas(self):
        rol_mean = self.mte.rolling(window = 12, center = False).mean()
        rol_std = self.mte.rolling(window = 12, center = False).std()

        return self.mte

    def getTrendsData(self):
        decomposition = seasonal_decompose(self.mte)

        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid

        return self.mte, trend, seasonal, residual 


if __name__ == "__main__":
    car = Carbon('dataset.csv')
    print(car.getMonthlyGreenGas())