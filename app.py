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
def index():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    print(ts)
    graphs = [
        dict(
            data=[ dict( x=[1, 2, 3], y=[10, 20, 30], type='scatter'),],
            layout=dict(title='first graph')
            ),

        dict( 
            data=[ dict( x=[1, 3, 5], y=[10, 50, 30], type='bar'), ],
            layout=dict( title='second graph')
            ),

        dict(
            data=[ dict( x=ts.index,  # Can use the pandas data structures directly
            y=ts)])
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           graphJSON=graphJSON )


@app.route('/plot1')
def plot1():
    graphs = []

    for desc, group in car.getEnergySources():
        graphs.append(
            dict(
                data = [dict(x = group.index, y = group.Value.values)]
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
                dict(x = group.index, y = group.Value.values, xaxis = f'x{index+1}', yaxis = f'y{index+1}')
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

if __name__ == '__main__':
    app.run(debug = True)
