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
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
])


# Function to create a graph container
def create_graph_container(graph_id, title, info_text):
    
    return html.Div([
        html.H3(title),  # Title on top
        html.Div([
            dcc.Graph(id=graph_id, style={'flex': '0 0 80%'}),  # Graph

            # Info button with hover text
            html.Div(
                children=[
                    html.Span("ℹ️", className="info-icon"),  # Using Unicode for info icon
                    html.Span(
                        info_text,
                        className="info-text"
                    )
                ],
                className="info-container",
                style={'flex': '0 0 20%', 'text-align': 'center', 'position': 'relative'}
            )
        ], style={'display': 'flex', 'align-items': 'center'}),  # Flexbox to align items horizontally
    ], className='graph-container')


#---------------------------------------------------------------------------------------------------





# Define the layout of the app using app.layout
app.layout = html.Div(children=[
    html.H1(children='Fruit Sales Dashboard'),

    html.Div(children='''
        A simple dashboard to display fruit sales data.
    '''),

    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[
                {'label': 'San Francisco', 'value': 'SF'},
                {'label': 'New York City', 'value': 'NYC'}
            ],
            value='SF'  # Default value
        ),
    ]),
    
    create_graph_container('fruit-sales-bar-chart',
                           "Graph 1: Fruit Sales in City", 
                           "This bar chart shows the sales amounts of different fruits in the selected city (Graph 1)."),

    create_graph_container('fruit-sales-pie-chart',
                           "Graph 2: Fruit Sales Pie in City", 
                           "This bar chart shows the sales amounts of different fruits in the selected city (Graph 1)."),

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
