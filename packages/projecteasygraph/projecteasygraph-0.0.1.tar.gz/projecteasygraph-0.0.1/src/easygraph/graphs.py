import plotly.graph_objects as go
from . import utils


def bar_graph(data, x_column, y_column: str | list, title=None, xaxis_title=None, yaxis_title=None, orientation='v'):
    fig = go.Figure()

    if orientation == 'v':
        if xaxis_title == None:
            xaxis_title = x_column

        if isinstance(y_column, str):
            if yaxis_title == None:
                yaxis_title = y_column
            utils.add_bar_trace(fig, data, x_column, y_column, '', orientation)
        elif isinstance(y_column, list):
            if yaxis_title == None:
                yaxis_title = ''
            for i in y_column:
                utils.add_bar_trace(fig, data, x_column, i, i, orientation)
        else:
            print("error")
    else:
        if yaxis_title == None:
            yaxis_title = x_column

        if isinstance(y_column, str):
            if xaxis_title == None:
                xaxis_title = y_column
            utils.add_bar_trace(fig, data, y_column, x_column, '', orientation)
        elif isinstance(y_column, list):
            if yaxis_title == None:
                yaxis_title = ''
            for i in y_column:
                utils.add_bar_trace(fig, data, i, x_column, i, orientation)
        else:
            print("errro")

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',

        width=700,
        height=700,
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )
    return fig


def histogram_graph(data, columns: str | list, title=None, axis_title='', orientation='v'):
    fig = go.Figure()
    if orientation == 'v':
        x_title = axis_title
        y_title = 'Count'
        if isinstance(columns, str):
            fig.add_trace(go.Histogram(x=data[columns], name=columns))
        elif isinstance(columns, list):
            for i in columns:
                fig.add_trace(go.Histogram(x=data[i], name=i))
    elif orientation == 'h':
        x_title = 'Count'
        y_title = axis_title
        if isinstance(columns, str):
            fig.add_trace(go.Histogram(y=data[columns], name=columns))
        elif isinstance(columns, list):
            for i in columns:
                fig.add_trace(go.Histogram(y=data[i], name=i))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        bargap=0,

        width=700,
        height=700,
        title=title,
        xaxis_title_text=x_title,
        yaxis_title_text=y_title,

    )
    return fig


def line_graph(data, x_column, y_column: str | list, title=None, xaxis_title=None, yaxis_title=None):
    fig = go.Figure()
    if xaxis_title == None:
        xaxis_title = x_column

    if isinstance(y_column, str):
        if yaxis_title == None:
            yaxis_title = yaxis_title
        fig.add_trace(go.Scatter(x=data[x_column], y=data[y_column]))

    if isinstance(y_column, list):
        for i in y_column:
            fig.add_trace(go.Scatter(x=data[x_column], y=data[i], name=i))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )

    return fig


def dispersion_graph(data, x_column, y_column: str | list, title=None, xaxis_title=None, yaxis_title=None):
    fig = go.Figure()
    if xaxis_title == None:
        xaxis_title = x_column
    if isinstance(y_column, str):
        if yaxis_title == None:
            yaxis_title = yaxis_title
        fig.add_trace(go.Scatter(
            x=data[x_column], y=data[y_column], mode='markers'))

    if isinstance(y_column, list):
        for i in y_column:
            fig.add_trace(go.Scatter(
                x=data[x_column], y=data[i], mode='markers', name=i))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )

    return fig


def box_plots(data, x_column: str | list = None, y_column=None, title=None, xaxis_title=None, yaxis_title=None):
    fig = go.Figure()

    if x_column != None:
        if isinstance(x_column, str):
            fig.add_trace(go.Box(x=data[x_column]))

        if isinstance(x_column, list):
            for i in x_column:
                fig.add_trace(go.Box(x=data[i], name=i))

    if y_column != None:
        if isinstance(y_column, str):
            fig.add_trace(go.Box(y=data[y_column]))

        if isinstance(y_column, list):
            for i in y_column:
                fig.add_trace(go.Box(y=data[i], name=i))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )

    return fig
