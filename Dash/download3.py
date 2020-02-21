import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dte
from flask import send_file
import io
import flask
import pandas as pd

import xlsxwriter

app = dash.Dash()
app.layout = html.Div(children=[
    html.A("download excel", href="/download_excel/"),
])

IRP2019_P = pd.read_excel('2019-IRP.xlsx',sheet_name="IRP1_P")

@app.server.route('/download_excel/')
def download_excel():
    #Create DF
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    print(df)
    # df= pd.DataFrame(IRP2019_P)
    # print(df)
    #Convert DF
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(df, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1")
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
                     attachment_filename='test45.xlsx',
                     as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)