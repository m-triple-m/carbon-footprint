from flask import Flask, render_template, jsonify
from processData import Carbon
from countryData import CountryData
import json
import plotly

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True
car = Carbon('datasets/dataset.csv')
con = CountryData('datasets/emission_data.csv')

@app.route('/')
@app.route('/home')
def index():
    
    return render_template('index.html')

@app.route('/plot1')
def plot1():
    graphs = []

    for desc, group in car.getEnergySources():
        graphs.append(
            dict(
                data = [dict(x = group.index, y = group.Value.values, name = desc)]
            )
        )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot2.html', graphJSON = graphJSON)

@app.route('/subplots')
def sub():
    graphs = []

    layout = {
        "grid": {"rows": 1, "columns": 2, "pattern": 'independent'},
        }

    for index, (desc, group) in enumerate(car.getEnergySources()):
        graphs.append(
            dict(
                dict(x = group.index, y = group.Value.values, name = desc, xaxis = f'x{index+1}', yaxis = f'y{index+1}')
            )
        )

    # print(graphs)

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('subplot.html', graphJSON = graphJSON)

@app.route('/bar')
def barChart():
    data = car.getCO2perSource()

    graphs = [dict(x = data.index, y = data.values, type = 'bar')]

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('barchart.html', graphJSON = graphJSON)

@app.route('/monthly')
def monthly():
    graphs = []

    data = car.getMonthlyGreenGas()
    graphs.append(
        dict(
            data = [dict(x = data.index, y = data.values)]
        )
    )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('monthly.html', graphJSON = graphJSON)

@app.route('/trend')
def trends():
    graphs = []


    for group, name in zip(car.getTrendsData(), ['original', 'trend', 'seasonal', 'residual']):
        graphs.append(
            dict(
                data = [dict(x = group.index, y = group.values, name = name)]
            )
        )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('trends.html', graphJSON = graphJSON)

@app.route('/country')
def CountryPlot():
    graphs = []

    df = con.getCountrydata()
    for column in df.columns[-20:]:
        graphs.append(
            dict(
                data = [dict(x = df['Country'], y = df[column], name = column)]
            )
        )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('trends.html', graphJSON = graphJSON)

@app.route('/world')
def worldPlot():
    graphs = []

    df = con.getCountrydata()
    graphs.append(
        dict(
            data = [dict(x = df.columns[50:], y = df.loc[df['Country'] == 'World'][df.columns[50:]].values.squeeze())]
        )
    )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('trends.html', graphJSON = graphJSON)

@app.route('/map')
def MapPlot():
    
    plot_df = con.getCountrydata()

    first_year = 1960
    last_year = 2011
    number_of_steps = int(2011 - 1960)

    # data is a list that will have one element for now, the first element is the value from the first year column we are interested in.
    data = [dict(type='choropleth',
                locations = plot_df['country_code'].astype(str),
                z=plot_df[str(first_year)].astype(float))]

    # next, we copy the data from the first cell, append it to the data list and set the data to the value contained in the year column of the dataframe.
    for i in range(number_of_steps):
        data.append(data[0].copy())
        index = str(first_year + i + 1)
        data[-1]['z'] = plot_df[index]

    graphJSON = json.dumps([dict(data = data)], cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('map.html', graphJSON = graphJSON)


@app.route('/topemitter')
def topEmitters():
    
    graphs = []

    df = con.getTopData(years = 10)

    data = df.sort_values(by = 'Total', ascending=False)[:21]

    graphs.append(
            dict(x = data['Country'], y = data['Total'], type = 'bar')
    )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('topemit.html', graphJSON = graphJSON)


@app.route('/year')
def yearWise():
    
    graphs = []

    df = con.getCountrydata()
    

    data = df.sort_values(by = '2017', ascending=False)[:41]

    graphs.append(
            dict(x = data['Country'], y = data['2017'], type = 'bar')
    )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('year.html', graphJSON = graphJSON)

@app.route('/devdata')
def Dev():

    graphs = []
    df = con.getCountrydata()
    print(df.columns)

    us = df.loc[df['Country'] == 'United States']
    india = df.loc[df['Country'] == 'India']

    graphs.append(
            dict(x = us.columns[2:-1],  y = us.iloc[0][2:-1].values, fill = 'tozeroy', name = "USA")
    )
    graphs.append(
            dict(x = india.columns[2:-1],  y = india.iloc[0][2:-1].values, fill = 'tozeroy', name = "INDIA")
    )

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify(graphJSON)

@app.route('/dev')
def devpage():

    return render_template('dev.html')

    

if __name__ == '__main__':
    app.run(debug = True)
