import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# dcc is dash core components -> higher-level components like graphs, dropdowns, sliders, etc.
# html is dash html component -> to use HTML tags directly in your Python code.
# Input, Output are used for linking interactive components (like dropdowns) to your app's functions. plotly.express is used to create quick and easy plots.

# Sample data for plotting
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Berries", "Grapes"],
    "Amount": [4, 2, 5, 7, 1],
    "City": ["SF", "SF", "SF", "NYC", "NYC"]
})

# Create a Dash application
app = dash.Dash(__name__)


# Define the layout of the app using app.layout
app.layout = html.Div(children=[
    html.H1(children='Fruit Sales Dashboard'),

    html.Div(children='''
        A simple dashboard to display fruit sales data.
    '''),

    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'San Francisco', 'value': 'SF'},
            {'label': 'New York City', 'value': 'NYC'}
        ],
        value='SF'  # Default value
    ),

    html.Div([
        dcc.Graph(id='fruit-sales-bar-chart'),

        # info button next to graph that will show text on hover
        html.Div(children="ℹ️")


    ]),

    dcc.Graph(id='fruit-sales-pie-chart')
])


# Define the callback to update the graph
# @app.callback is the core of Dash's interactivity. 
# It links user inputs (like the dropdown selection) to outputs (like the graph).
# When the user selects a different city, the graph updates automatically.
@app.callback(
    Output('fruit-sales-bar-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_figure(selected_city):
    filtered_df = df[df['City'] == selected_city]
    fig = px.bar(filtered_df, x="Fruit", y="Amount", title=f'Fruit Sales in -> {selected_city}')
    return fig


@app.callback(
    Output('fruit-sales-pie-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_pie_chart(selected_city):
    filtered_df = df[df['City'] == selected_city]
    pie_fig = px.pie(filtered_df, names="Fruit", values="Amount", title=f'Sales Distribution in {selected_city}')
    return pie_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
