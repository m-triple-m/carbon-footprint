import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pylab
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams


class Carbon:
    def __init__(self, path):

        dateparse = lambda x: pd.to_datetime(x, format='%Y%m', errors = 'coerce')
        df = pd.read_csv(path, parse_dates=['YYYYMM'], index_col='YYYYMM', date_parser=dateparse)

        self.ts = df[pd.Series(pd.to_datetime(df.index, errors='coerce')).notnull().values]

        self.ts['Value'] = pd.to_numeric(self.ts['Value'] , errors='coerce')

        

    def getEnergySources(self):
        return self.ts.groupby('Description')

    def getCO2perSource(self):
        return self.ts.groupby('Description')['Value'].sum().sort_values()


if __name__ == "__main__":
    car = Carbon('dataset.csv')
    for desc, group in car.getEnergySources():
        print(desc)