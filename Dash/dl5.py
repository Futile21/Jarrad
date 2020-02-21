import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dte
from flask import send_file
import io
import flask
import pandas as pd
import urllib
import base64

IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")


app = dash.Dash()
app.layout = html.Div([
        html.A(
            'Download Data',
            id='download-link',
            download="table.xls",
            href="",
            target="_blank"
        ),
    html.A(
        'Download Excel Data',
        id='download-link',
        download="data.xlsx",
        href="",
        target="_blank"
    )
])

@app.callback(
    Output('excel-download', 'href'),
    [Input('download-link', 'value')])
def update_download_button(value):
    df = IRP2019_P
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="period")
    writer.save()
    xlsx_io.seek(0)
    # https://en.wikipedia.org/wiki/Data_URI_scheme
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    return href_data_downloadable

if __name__ == '__main__':
    app.run_server(debug=True)