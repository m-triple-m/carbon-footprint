import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CountryData:

    def __init__(self, dataPath):
        self.df = pd.read_csv(dataPath)

    def getCountrydata(self):
        return self.df

    def getTopData(self, years = 50):
        data = self.df
        data['Total'] = data[data.columns[-years:]].sum(axis = 1)

        return data
    
    def getYearDat(self, year = 2017):
        data = self.df
        