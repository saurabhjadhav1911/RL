import dash
from dash.dependencies import Output, Input, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
#import argparse
#import sys
from threading import Thread
import threading
from colorama import Fore, Back, Style
import colorama
#import multiprocessing
import numpy as np
#from misc import *
import time
#import cv2
#import sys
#import os
#import traceback
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import LSTM
#import tensorflow as tf
#import matplotlib.pyplot as plt
#import socket
#import traceback

X = deque(maxlen=100)
X.append(1)

Y = deque(maxlen=100)
Y.append(1)

YM = deque(maxlen=100)
YM.append(1)

T = deque(maxlen=100)
T.append(1)

data_dict = {'X': X, 'Y': Y, 'T': T, 'YM': YM}
color = Fore.BLUE

colorama.init()

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
            html.H2('Single Servo Sim Data', style={
                'float': 'left',
            }),
        ]),
        dcc.Dropdown(
            id='single_servo_sim_graph',
            options=[{
                'label': s,
                'value': s
            } for s in data_dict.keys()],
            value=['X','Y','YM'],
            multi=True),
        html.Div(children=html.Div(id='graphs'), className='row'),
        dcc.Interval(id='graph-update', interval=100),
    ],
    className="container",
    style={
        'width': '98%',
        'margin-left': 10,
        'margin-right': 10,
        'max-width': 50000
    })


@app.callback(
    Output('graphs', 'children'), [Input('single_servo_sim_graph', 'value')],
    events=[Event('graph-update', 'interval')])
def update_graph_scatter(data_names):

    graphs = []

    update_data()

    if len(data_names) > 2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:

        data = go.Scatter(
            x=list(T),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb")

        graphs.append(
            html.Div(
                dcc.Graph(
                    id=data_name,
                    animate=True,
                    figure={
                        'data': [data],
                        'layout':
                        go.Layout(
                            xaxis=dict(
                                range=[min(T), max(T)]),
                            yaxis=dict(range=[
                                min(data_dict[data_name]),
                                max(data_dict[data_name])
                            ]),
                            margin={'l': 50,
                                    'r': 1,
                                    't': 45,
                                    'b': 1},
                            title='{}'.format(data_name))
                    }),
                className=class_choice))

    return graphs


def update_data():
    data_dict['T'].append(T[-1] + 1)
    data_dict['X'].append(X[-1] + X[-1] * random.uniform(-0.1, 0.1))
    data_dict['YM'].append(YM[-1] + YM[-1] * random.uniform(-0.1, 0.1))
    data_dict['Y'].append(Y[-1] + Y[-1] * random.uniform(-0.1, 0.1))


if __name__ == '__main__':

    #update_thread = Thread(target=update_data)
    app.run_server(debug=True)
    #update_thread.start()

    #update_thread.join()
