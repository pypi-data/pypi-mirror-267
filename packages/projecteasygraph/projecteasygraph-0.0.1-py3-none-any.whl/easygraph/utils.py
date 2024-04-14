import plotly.graph_objects as go


def add_bar_trace(fig: go.Figure, data, x_column, y_column, name, orientation):
    fig.add_trace(go.Bar(
        x=data[x_column],
        y=data[y_column],
        name=name,
        orientation=orientation
    ))
