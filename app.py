from flask import Flask, render_template
from processData import Carbon
import json
import plotly

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True
car = Carbon('dataset.csv')

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

    return render_template('plot2.html', graphJSON = graphJSON)

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


if __name__ == '__main__':
    app.run(debug = True)
