import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    'Dash tesdfgfgt',
    dcc.Graph(
        id='eg',
        figure={
            'data': [{
                'x': [1, 2, 3, 4],
                'y': [4, 5, 6, 7],
                'type': 'line',
                'name': 'boats'
            }]
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)