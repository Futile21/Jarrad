import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import urllib
import io
import base64

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [2, 1, 5, 6],
    'c': ['x', 'x', 'y', 'y']
})

IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash(__name__)
app.layout = html.Div([
    html.Label('Filter'),

    dcc.Dropdown(
        id='field-dropdown',
        options=[
            {'label': i, 'value': i} for i in
            (['all'] + list(df['c'].unique()))],
        value='all'
    ),
    html.Div(id='table'),
    html.A(
        'Download Data',
        id='download-link',
        download="test.xlsx",
        href="",
        target="_blank"
    )
])


def filter_data(value):
    if value == 'all':
        return df
    else:
        return df[df['c'] == value]


@app.callback(
    dash.dependencies.Output('table', 'children'),
    [dash.dependencies.Input('field-dropdown', 'value')])
def update_table(filter_value):
    dff = filter_data(filter_value)
    return generate_table(dff)


# @app.callback(
#     dash.dependencies.Output('download-link', 'href'),
#     [dash.dependencies.Input('field-dropdown', 'value')])
# def update_download_link(filter_value):
#     dff = IRP2019_P
#     csv_string = dff.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
#     return csv_string


@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('field-dropdown', 'value')])
def update_download_link(filter_value):
    df = IRP2019_P
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
    df.to_excel(writer,index=False, sheet_name="period")
    writer.save()
    xlsx_io.seek(0)
    # https://en.wikipedia.org/wiki/Data_URI_scheme
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    return href_data_downloadable



if __name__ == '__main__':
    app.run_server(debug=True)