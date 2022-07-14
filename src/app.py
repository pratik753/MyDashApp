# from tkinter.ttk import Style
from pydoc import classname
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html
import matplotlib.pyplot as plt
from dash.dependencies import Output, Input, State
import os
import base64
# import dash_bootstrap_components as dbc
# from google.cloud import storage
#import ipynb.fs.full.function_file as fun
import function_file as fun
import pyrebase
# import re

firebaseConfig = {
    "apiKey": "AIzaSyDA5rJY0xgufybKyRLhgIPEJ-l39AqRV_g",
    "authDomain": "dash-5784a.firebaseapp.com",
    "projectId": "dash-5784a",
    "storageBucket": "dash-5784a.appspot.com",
    "messagingSenderId": "7529769290",
    "appId": "1:7529769290:web:26c9c181ad4d334a83f9b3",
    "measurementId": "G-2NGWD4QDFZ",
    "databaseURL": "gs://dash-5784a.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)


def defCall():
    bookPath = "https://firebasestorage.googleapis.com/v0/b/dash-5784a.appspot.com/o/Book3.xlsx?alt=media"
    Item_file_1 = "https://firebasestorage.googleapis.com/v0/b/dash-5784a.appspot.com/o/Item_file_1.xlsx?alt=media&token=7d8f093c-2b02-4f48-ab55-8f171386afbb"
    Trade_File_1 = "https://firebasestorage.googleapis.com/v0/b/dash-5784a.appspot.com/o/Trade_File_1.xlsx?alt=media&token=933fef62-f747-4b70-91e9-af77782e0abb"
    df_new = pd.read_excel(bookPath)
    df_new.drop(df_new[df_new['Transaction Type']
                == 'Deposit'].index, inplace=True)
    df_new.reset_index(drop=True, inplace=True)
    df_trade = pd.read_excel(Item_file_1)
    df_item = pd.read_excel(Trade_File_1)
    df_item.columns = ['Product/Service', 'Category']
    #   return df_new, df_trade, df_item

    return df_new, df_trade, df_item


# df_new, df_trade, df_item = refreshFunction()
# external JavaScript files
external_scripts = [
    # 'https://www.google-analytics.com/analytics.js',
    # {'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js'},
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor',
        'crossorigin': 'anonymous'
    },
    'https://www.w3schools.com/w3css/4/w3.css'
]

app = Dash(__name__, external_scripts=external_scripts,
           external_stylesheets=external_stylesheets)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


def table(data):
    t = list(data.columns)
    tab = dash.dash_table.DataTable(

        [{"_".join(col): val for col, val in row.items()}
         for row in data.to_dict('records')],
        id="tableDash",
        columns=[{"name": col, "id": "_".join(col)} for col in data.columns],
        style_table={'overflowX': 'auto',
                     'overflowY': 'auto', 'padding': '2rem', 'paddingBottom': "1.2rem"},
        style_cell={
            'height': 30,
            'minWidth': '90px', 'width': '90px', 'maxWidth': '150px',
            'whiteSpace': 'normal',
            'textAlign': 'center'
        },
        merge_duplicate_headers=True,
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#055979',
            'color': 'white'
        },
        style_data={
            # 'backgroundColor': 'white',
            'color': 'black'
        }
    )

    return tab


fig_plot = html.Div(id='fig_plot')
fig_plot1 = html.Div(id='fig_plot1')
fig_plot2 = html.Div(id='fig_plot2')
fig_dropdown1 = dcc.Dropdown(
    id='fig_dropdown1',
    value=None,
    placeholder='Item Set',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in ['Trade', 'Category']  # 'Customer',
    ]
)

fig_dropdown = dcc.Dropdown(
    id='fig_dropdown',
    value=None,
    placeholder='Filter',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in ['MTD', 'Custom', 'Quarter', 'Past 6 Months', 'Past 12 months']
    ])
date_dropdown1 = dcc.Dropdown(
    id='date_dropdown1',
    value='Jan',
    placeholder='Month',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in ['Jan', 'Feb', 'March', 'Apr', 'May', 'June',
                     'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ])
date_dropdown2 = dcc.Dropdown(
    id='date_dropdown2',
    value=2021,
    placeholder='year',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in range(2020, dt.datetime.now().year+1)
    ])
Quarter1 = dcc.Dropdown(
    id='Quarter1',
    value='Q4',
    placeholder='Q4',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in ['Q1', 'Q2', 'Q3', 'Q4']
    ])
Quarter2 = dcc.Dropdown(
    id='Quarter2',
    value=2021,
    placeholder='year',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in range(2020, dt.datetime.now().year+1)
    ])
Quarter2qq = dcc.Dropdown(
    id='Quarter2qq',
    value=2021,
    placeholder='year',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in range(2020, dt.datetime.now().year+1)
    ])
table_graph = dcc.Dropdown(
    id='table_graph',
    value='Relative',
    placeholder='Table/Graph',
    clearable=False,
    searchable=False,
    options=[
        {'label': name, 'value': name}
        for name in ['Relative', 'Absolute']
    ], )
date_mtd2 = dcc.DatePickerSingle(
    id='date2',
    min_date_allowed=dt.date(1995, 8, 5),
    max_date_allowed=dt.datetime.now().date(),
    initial_visible_month=dt.datetime.now().date(),
    date=dt.datetime(2021, 9, 1).date(),
    display_format='DD/MM/YYYY',
    # style={'padding': '3px 6px'}
)
date_mtd3 = dcc.DatePickerSingle(
    id='date3',
    min_date_allowed=dt.date(1995, 8, 5),
    max_date_allowed=dt.datetime.now().date(),
    initial_visible_month=dt.datetime.now().date(),
    date=dt.datetime(2021, 12, 1).date(),
    display_format='DD/MM/YYYY',
    # style={'padding': '3px 6px'}
)
password = html.Div([dcc.Input(
    id='password',
    type="password",
    placeholder='PASSWORD')
], className="passwordDiv")
button = html.Div([html.Button('Submit', id='button1', n_clicks=0)])
output = html.Div(id='output', children=[
    html.Div([html.H5(children='Password'), html.Div([password], className="mtdDiv")],
             className="col sideBarDrop"),
    html.Div([html.Div([button], className="mtdDiv")],
             className="col sideBarDrop")])

outputText = html.Div(id="outputText")


uploadFile = dcc.Upload(id="uploadData", children=html.Button('Upload File'))

uploadButton = html.Button('Apply', id='apply_button', n_clicks=0)
passwordInput = html.Div(dcc.Input(id="passwordInput", type="text"))
# def uploadFile():
#     print("hii")

sideBar = html.Div([
    html.Ul([
        html.Div([

            html.Div([
                html.Div([fig_dropdown1], className="col sideBarDrop"),
                html.Div([fig_dropdown], className="col sideBarDrop"),
                html.Div([html.H5(children='MTD'),
                          html.Div([date_dropdown1, date_dropdown2], className="mtdDiv")],
                     className="col sideBarDrop"),
                html.Div([html.H5(children='Initial Date for Custom'),
                 html.Div([date_mtd2], className="mtdDiv")],
                     className="col sideBarDrop"),
                html.Div([html.H5(children='Final date for Custom'),
                          html.Div([date_mtd3], className="mtdDiv")],
                     className="col sideBarDrop"),
                html.Div([html.H5(children='Quarter'),
                          html.Div([Quarter1, Quarter2], className="mtdDiv")],
                     className="col sideBarDrop"),
                # html.Div([html.H5(children='Password'),
                #           html.Div([password], className="mtdDiv")],
                #      className="col sideBarDrop"),
                # html.Div([html.Div([ button], className="mtdDiv")],
                #      className="col sideBarDrop"),
                html.Div([html.Div([html.Div([output], className="mtdDiv")],
                     className="col sideBarDrop"),
                          ]),
                html.Div([html.Div([html.Div([outputText], className="mtdDiv")],
                     className="col sideBarDrop"),
                          ])

            ], className="row"),

        ], className='sideBarList')

    ], className="w3-ul myli"),
], className="sideBar")

navBar = html.Div(
    [html.Span(["Analytics Panel"], className="navText")], className="navBar")

# alertDiv= dbc.Alert("This is a danger alert. Scary!", color="danger"),
# fig_dropdown1
app.layout = html.Div([
    navBar,
    sideBar,
    # alertDiv,
    html.Div([
        html.H2(children="Consolidated Table followed by Graph",
                className="graphTitle"),
        html.Div([table_graph], className="table_graph"),
        html.Div([uploadButton,
                 passwordInput], className="displayNone"),
        html.Div([

            fig_plot1, fig_plot, fig_plot2,
        ], className="table_graphDiv")
    ], className="container mainCont divContCenter"),
    html.Div([dcc.Store(id='store_data1', data=[], storage_type='memory'),
              dcc.Store(id='store_data2', data=[], storage_type='memory'),
              dcc.Store(id='store_data3', data=[], storage_type='memory'),
              dcc.Store(id='store_data4', data=[], storage_type='memory'),
              ])
])


def uploadFunction(contents, filename, date):
    # create simplest BytesIO object
    #   storage=firebase.storage()
    # b = io.BytesIO(b'hello')
    # create storage client
    # storage_client = storage.Client()
    # create test bucket
    # bucket = storage_client.bucket("vittoh-test-bytesio")
    # create test blob
    # blob = bucket.blob("vitooh-test-blob")
    # upload with type zip
    # client = storage.Client()
    # bucket = client.bucket("bucket-name")
    # blob = bucket.blob("vitooh-test-blob")
    # blob.upload_from_string(contents,content_type='application/xlsx')

    storage = firebase.storage()
    file = "D:\pratik\Book3.xlsx"
    cloudfilename = filename
    print(os.path.basename(filename))
    get_file_content = contents
    # upload a file
    # file=input("Enter the name of the file you want to upload to storage")
    # cloudfilename=input("Enter the name for the file in storage")
    data = contents
    # altchars=b'+/'
    # data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    # missing_padding = len(data) % 4
    # if missing_padding:
    # data += b'='* (4 - missing_padding)
    # lens = len(data)
    # lenx = lens - (lens % 4 if lens % 4 else 4)
    name = "Book3.xlsx"
    decode_content = base64.b64decode(data.split(',')[1])
    # base64.b64decode(data, altchars)
    storage.child(name).put(decode_content)
    # blob.upload_from_string(contents, content_type='image/png')
    # get url of the file we just uploaded
    bookPath = storage.child(cloudfilename).get_url(None)
    print(storage.child(cloudfilename).get_url(None))
    print(filename, date)
    # df_new, df_trade, df_item = refreshFunction()
    return


@ app.callback(Output('output', 'children'),
               Output('outputText', 'children'),
               Output('button1', 'n_clicks'),
               Input('password', 'value'),
               Input('button1', 'n_clicks'))
def check_password(pas, clicks):
    if clicks > 0:
        if pas == '1234':
            return html.Div(children=[uploadFile, ""]), html.H4("Correct"), 0
            # return html.Div([ children=[uploadFile]]), 0
        else:
            return html.Div(children=[output, ""]), html.H5("InCorrect"), 0

# def check_passwordText(pas, clicks):
#     if clicks > 0:
#         if pas == '1234':
#             return  0
#         else:
#             return html.Div("incorrect"), 0


@ app.callback(
    Output('store_data1', 'data'),
    Output('store_data2', 'data'),
    Output('store_data3', 'data'),
    #    Output('button1','n_clicks'),
    #   Input('password','value'),
    #   Input('button1','n_clicks'),
    Input('apply_button', 'n_clicks'),
    Input('uploadData', 'contents'),
    State('uploadData', 'filename'),
    State('uploadData', 'last_modified'),
)
def check_password(click, c, n, d):
    if click >= 1 or n is not None:
        # children = [
        uploadFunction(c, n, d)
        #
        bookPath = "https://firebasestorage.googleapis.com/v0/b/dash-5784a.appspot.com/o/Book3.xlsx?alt=media"
        # bookPath = "./book2.xlsx"
        df = pd.read_excel(bookPath)
        df.drop(df[df['Transaction Type'] == 'Deposit'].index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df_trade = pd.read_excel(
            './Item_file_1.xlsx')
        df_item = pd.read_excel(
            './Trade_File_1.xlsx')
        df_item.columns = ['Product/Service', 'Category']
        # df['day'] = pd.to_datetime(
        # df['Date'], format="%d-%m-%Y").dt.day  # inegrate
        # df['Date_month'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.month
        # df['Date_year'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.year
        # df['Date_Month1'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.month
        # day = []
        # for i in range(len(df)):
        #     x1 = str(df['Date_year'][i])+'-'+str(df['Date_month'][i]) + \
        #         '-'+str(df['day'][i])
        #     day.append(x1)
        # df['day'] = day
        # df['Date_Month1'].replace({1: 'Jan', 2: 'Feb', 3: 'March', 4: 'Apr', 5: 'May', 6: 'June',
        #                         7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}, inplace=True)  # inegrate
        # # df.drop(['Qty', 'Sales Price'], axis=1, inplace=True)
        df_new = df.copy()
    #   return df_new, df_trade, df_item

        return df_new.to_dict('records'), df_trade.to_dict('records'), df_item.to_dict('records')


@ app.callback(Output('fig_plot1', 'children'),
               Output('fig_plot', 'children'),
               Output('fig_plot2', 'children'),
               Output('store_data4', 'data'),
               Input('fig_dropdown1', 'value'),
               Input('fig_dropdown', 'value'),
               Input('date_dropdown1', 'value'),
               Input('date_dropdown2', 'value'),
               Input('date2', 'date'),
               Input('date3', 'date'),
               Input('Quarter1', 'value'),
               Input('Quarter2', 'value'),
               Input('table_graph', 'value'),
               State('store_data1', 'data'),
               State('store_data2', 'data'),
               State('store_data3', 'data'),
               #   Input("passwordInput", "value"),
               )
def update_output(fig_dropdown1, fig_dropdown,  date_m, date_y, date2, date3, in1, in2, input3, s1, s2, s3):
    return name_to_figure(fig_dropdown1, fig_dropdown, date_m, date_y, date2, date3, in1, in2, input3, s1, s2, s3)


def name_to_figure(fig_dropdown1, fig_dropdown,  date_m, date_y, date2, date3, in1, in2, input3, s1, s2, s3):

    mon = {1: 'Jan', 2: 'Feb', 3: 'March', 4: 'Apr', 5: 'May', 6: 'June',
           7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    figure = go.Figure()
    figure1 = go.Figure()
    figure2 = go.Figure()
    figure3 = ''
    figure4 = ''
    df_new = pd.DataFrame()
    df_trade = pd.DataFrame()
    df_item = pd.DataFrame()

    x1 = pd.DataFrame()
    if(len(list(pd.DataFrame(s1).columns)) != 0):
        print("hii 2")
        df_new = pd.DataFrame(s1)
        print(df_new.columns)
        df_trade = pd.DataFrame(s2)
        df_item = pd.DataFrame(s3)
    else:
        print("hii")
        df_new, df_trade, df_item = defCall()
    df_new['day'] = pd.to_datetime(
        df_new['Date'], format="%Y-%m-%d").dt.day  # inegrate
    df_new['Date_month'] = pd.to_datetime(
        df_new['Date'], format="%Y-%m-%d").dt.month
    df_new['Date_year'] = pd.to_datetime(
        df_new['Date'], format="%Y-%m-%d").dt.year
    df_new['Date_Month1'] = pd.to_datetime(
        df_new['Date'], format="%Y-%m-%d").dt.month
    day = []

    for i in range(len(df_new)):
        x1 = str(df_new['Date_year'][i])+'-' + \
            str(df_new['Date_month'][i]) + '-'+str(df_new['day'][i])
        day.append(x1)
    df_new['day'] = day
    df_new['Date_Month1'].replace({1: 'Jan', 2: 'Feb', 3: 'March', 4: 'Apr', 5: 'May', 6: 'June',
                                   7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}, inplace=True)  # inegrate
    # df_new.drop(['Qty', 'Sales Price'], axis=1, inplace=True)
    merg = df_trade
    # if fig_dropdown1 == 'Customer':
    #   inpt = 'Customer'
    if fig_dropdown1 == 'Trade':
        inpt = 'Trade'
        merg = df_trade
    elif fig_dropdown1 == 'Category':
        inpt = 'Category'
        merg = df_item
    if fig_dropdown == 'MTD':
        s1 = date_m+'-'+str(date_y)
        t1, x1, c1 = fun.MTD(df_new, inpt, s1, merg, 10)
        total = fun.changeP(c1['Amount'].sum())
        total1 = fun.changeP(x1['Amount'].sum())
        c1.drop('Amount', axis=1, inplace=True)
        figure = table(c1)
        figure = html.Div([figure, html.H2("Month", className="percentTitle")])
        figure1 = px.bar(x1, x='Month', y="Amount", color=inpt, text='Amount (Rs.)',
                         width=900, height=550, hover_data=['Amount (Rs.)', 'Sale_Amount (%)'])
        figure1.update_traces(textposition='inside')
        figure1.update_traces(marker_color='#119dff')
        # figure1.update_layout(title='Month')
        figure2 = px.bar(c1, x=inpt, y='Sale_Amount (%)',
                         width=900, hover_data=['Amount (Rs.)'])
        figure2.update_layout(yaxis={'categoryorder': 'total descending'})
        figure2.update_traces(marker_color='#119dff')
        figure3 = table(t1)
        figure3 = html.Div(
            [figure3, html.H2("Months", className="percentTitle")])
        t1.drop('Amount(Rs.)', axis=1, level=1, inplace=True)
        mon = list(t1.columns.get_level_values(0))[1:]
        mon.insert(0, inpt)
        t1.columns = pd.MultiIndex.from_product([['Amount(%)'], mon])
        figure4 = table(t1)
        figure4 = html.Div([
            html.H2("Percentage Scale", className="percentTitle"), figure4])
    elif fig_dropdown == 'Custom':
        d1 = dt.date.fromisoformat(date2)
        d2 = dt.date.fromisoformat(date3)
        s1 = str(d1.year)+'-'+str(d1.month)+'-'+str(d1.day)
        s2 = str(d2.year)+'-'+str(d2.month)+'-'+str(d2.day)
        t1, x1, c1 = fun.CUSTOM_MONTH(df_new, inpt, s1, s2, merg, 10)
        total = fun.changeP(c1['Amount'].sum())
        total1 = fun.changeP(x1['Amount'].sum())
        c1.drop('Amount', axis=1, inplace=True)
        figure = table(c1)
        figure = html.Div(
            [figure, html.H2("Custom", className="percentTitle")])
        figure1 = px.bar(x1, x='Month', y="Amount", color=inpt, text='Amount (Rs.)',
                         width=900, height=550, hover_data=['Amount (Rs.)', 'Sale_Amount (%)'])
        figure1.update_traces(textposition='inside')
        figure1.update_traces(marker_color='#119dff')
        # figure1.update_layout(title='Custom')
        figure2 = px.bar(c1, x=inpt, y='Sale_Amount (%)',
                         width=900, hover_data=['Amount (Rs.)'])
        figure2.update_layout(yaxis={'categoryorder': 'total descending'})
        figure2.update_traces(marker_color='#119dff')
        figure3 = table(t1)
        figure3 = html.Div(
            [figure3, html.H2("Custom", className="percentTitle")])
        t1.drop('Amount(Rs.)', axis=1, level=1, inplace=True)
        mon = list(t1.columns.get_level_values(0))[1:]
        mon.insert(0, inpt)
        t1.columns = pd.MultiIndex.from_product([['Amount(%)'], mon])
        figure4 = table(t1)
        figure4 = html.Div([
            html.H2("Percentage Scale", className="percentTitle"), figure4])
        # figure4 =newDiv
    elif fig_dropdown == 'Quarter':
        t1, x1, c1 = fun.QUARTER(
            df_new, inpt, in1, in2, merg, 10)
        total = fun.changeP(c1['Amount'].sum())
        total1 = fun.changeP(x1['Amount'].sum())
        c1.drop('Amount', axis=1, inplace=True)
        figure = table(c1)
        figure = html.Div(
            [figure, html.H2("Quarter", className="percentTitle")])
        figure1 = px.bar(x1, x='Month', y="Amount", color=inpt, text='Amount (Rs.)',
                         width=900, height=550, hover_data=['Amount (Rs.)', 'Sale_Amount (%)'])
        figure1.update_traces(textposition='inside')
        figure1.update_layout(barmode='stack', height=500)
        figure1.update_traces(marker_color='#119dff')
        figure2 = px.bar(c1, x=inpt, y='Sale_Amount (%)',
                         width=900, hover_data=['Amount (Rs.)'])
        figure2.update_layout(yaxis={'categoryorder': 'total descending'})
        figure2.update_traces(marker_color='#119dff')
        figure3 = table(t1)
        figure3 = html.Div(
            [figure3, html.H2("Quarter", className="percentTitle")])
        t1.drop('Amount(Rs.)', axis=1, level=1, inplace=True)
        mon = list(t1.columns.get_level_values(0))[1:]
        mon.insert(0, inpt)
        t1.columns = pd.MultiIndex.from_product([['Amount(%)'], mon])
        figure4 = table(t1)
        figure4 = html.Div([
            html.H2("Percentage Scale", className="percentTitle"), figure4])

    elif fig_dropdown == 'Past 6 Months':
        t1, x1, c1 = fun.PAST_6_12_MON(df_new, inpt, merg, 6, 10)
        total = fun.changeP(c1['Amount'].sum())
        total1 = fun.changeP(x1['Amount'].sum())
        c1.drop('Amount', axis=1, inplace=True)
        figure = table(c1)
        figure = html.Div(
            [figure, html.H2("Past 6 Months", className="percentTitle")])
        figure1 = px.bar(x1, x='Month', y="Amount", color=inpt, text='Amount (Rs.)',
                         width=900, height=700, hover_data=['Amount (Rs.)', 'Sale_Amount (%)'])
        figure1.update_traces(textposition='inside')
        figure1.update_traces(marker_color='#119dff')
        figure2 = px.bar(c1, x=inpt, y='Sale_Amount (%)',
                         hover_data=['Amount (Rs.)'])
        figure2.update_layout(yaxis={'categoryorder': 'total descending'})
        figure2.update_traces(marker_color='#119dff')
        figure3 = table(t1)
        figure3 = html.Div(
            [figure3, html.H2("Past 6 Months", className="percentTitle")])
        t1.drop('Amount(Rs.)', axis=1, level=1, inplace=True)
        mon = list(t1.columns.get_level_values(0))[1:]
        mon.insert(0, inpt)
        t1.columns = pd.MultiIndex.from_product([['Amount(%)'], mon])
        figure4 = table(t1)
        figure4 = html.Div([
            html.H2("Percentage Scale", className="percentTitle"), figure4])
    elif fig_dropdown == 'Past 12 months':
        t1, x1, c1 = fun.PAST_6_12_MON(df_new, inpt, merg, 12, 10)
        total = fun.changeP(c1['Amount'].sum())
        total1 = fun.changeP(x1['Amount'].sum())
        c1.drop('Amount', axis=1, inplace=True)
        figure = table(c1)
        figure = html.Div(
            [figure, html.H2("Past 12 Months", className="percentTitle")])
        figure1 = px.bar(x1, x='Month', y="Amount", color=inpt, text='Amount (Rs.)',
                         width=900, height=550, hover_data=['Amount (Rs.)', 'Sale_Amount (%)'])
        figure1.update_traces(textposition='inside')
        # figure1.update_layout(title='Past 12 Months')
        figure2 = px.bar(c1, x=inpt, y='Sale_Amount (%)',
                         width=900, hover_data=['Amount (Rs.)'])
        figure2.update_layout(yaxis={'categoryorder': 'total descending'})
        figure2.update_traces(marker_color='#119dff')
        figure3 = table(t1)
        figure3 = html.Div(
            [figure3, html.H2("Past 12 Months", className="percentTitle")])
        t1.drop('Amount(Rs.)', axis=1, level=1, inplace=True)
        mon = list(t1.columns.get_level_values(0))[1:]
        mon.insert(0, inpt)
        t1.columns = pd.MultiIndex.from_product([['Amount(%)'], mon])
        figure4 = table(t1)
        figure4 = html.Div([
            html.H2("Percentage Scale", className="percentTitle"), figure4])

    inpt_drop = dcc.Dropdown(
        id='inpt_drop',
        value=None,
        placeholder='--select--',
        clearable=False,
        options=[
            {'label': name, 'value': name}
            for name in list(x1[inpt].unique())
        ])
    inpt_drop1 = dcc.Dropdown(
        id='inpt_drop1',
        value=None,
        placeholder='--select--',
        clearable=False,
        options=[
            {'label': name, 'value': name}
            for name in ['Amount (Rs.)', 'Sale_Amount (%)']
        ])
    config = {'displayModeBar': False}
    if input3 == 'Relative':
        return figure3, dcc.Graph(figure=figure1, config=config), figure4,  x1.to_dict('records')
    elif input3 == 'Absolute':
        return figure, dcc.Graph(figure=figure2, config=config), "", ""


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
