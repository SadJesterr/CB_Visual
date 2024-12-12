from xmlParser import XmlParser
from web import WebCbr
from graphBuilder import GraphBuilder

from dash import Dash, dcc, html, Input, Output, ctx
from dash.exceptions import PreventUpdate

CB = WebCbr()
VNAMES = XmlParser().get_vnames()


app = Dash()


app.layout = html.Div([
    html.H4('Интерактивные данные по времени'),
    html.P("Выберите валюту:"),
    dcc.Dropdown(
        id="curse_dropdown",
        options=VNAMES,
        value=VNAMES[0],
        clearable=True,
    ),
    dcc.DatePickerRange(id='curse_date'),
    html.Button('Подтвердить', id='button_curs_val', n_clicks=0),
    dcc.Graph(id="graph_curs",
              style={
                  'display': 'none'
              }),

    html.P("Выберите период динамики ключевой ставки:"),
    dcc.DatePickerRange(id='key_rate_date'),
    html.Button('Подтвердить', id='button_key_rate', n_clicks=0),
    dcc.Graph(id="graph_key_rate",
              style={
                  'display': 'none'
              }),
    
    html.P("Выберите период динамики стоимости драгоценных металлов:"),
    dcc.DatePickerRange(id='drag_met_date'),
    html.Button('Подтвердить', id='button_drag_met', n_clicks=0),
    dcc.Graph(id="graph_drag_met_date",
              style={
                  'display': 'none'
              }),
])

@app.callback(
    Output("graph_curs", "figure"), 
    Output("graph_curs", "style"),
    
    Input('button_curs_val', 'n_clicks'),
    Input("curse_dropdown", "value"),
    Input('curse_date', 'start_date'),
    Input('curse_date', 'end_date'),
    Input('graph_curs', 'figure'),
    Input('graph_curs', 'style'),
)
def updateGraphCurs(curs_n_clicks, value, start_date, end_date, 
                oldFigureCursDate, oldStyleCursDate
                ):
    styleCurs = oldStyleCursDate  # Изначально скрыт
    figureCurs = {}


    if 'button_curs_val' == ctx.triggered_id:
        if not value or not start_date or not end_date:
            raise PreventUpdate  # Не обновляем график, если поля пустые

        vCommoncode = XmlParser().get_common_code(value)
        curseFilename = f'{vCommoncode}-{start_date}-{end_date}.xml'

        CB.get_curse_dynamic_xml(start_date, end_date, vCommoncode)
        figureCurs = GraphBuilder().make_graph_from_curse(curseFilename, vCommoncode)
        styleCurs = {'display': 'block'}

    return figureCurs, styleCurs

@app.callback(
    Output("graph_key_rate", "figure"), 
    Output("graph_key_rate", "style"),

    Input('button_key_rate', 'n_clicks'),
    Input('key_rate_date', 'start_date'),
    Input('key_rate_date', 'end_date'),
    Input('graph_key_rate','figure'),
    Input('graph_key_rate','style')
)
def updateGraphKeyRate(key_rate_n_clicks, key_rate_start_date, key_rate_end_date, 
                oldFigureKeyRate, oldStyleKeyRate,
                ):
    figureKeyRate = {}
    styleKeyRate = oldStyleKeyRate  # Изначально скрыт
    
    if 'button_key_rate' == ctx.triggered_id:
        if not key_rate_start_date or not key_rate_end_date:
            raise PreventUpdate  # Не обновляем график, если поля пустые

        curseFilename = f'{key_rate_start_date}-{key_rate_end_date}.xml'
        CB.get_key_rate_xml(key_rate_start_date, key_rate_end_date)
        figureKeyRate = GraphBuilder().make_graph_from_key_rate(curseFilename)
        styleKeyRate = {'display': 'block'}

    return figureKeyRate, styleKeyRate

@app.callback(
    Output("graph_drag_met_date", "figure"), 
    Output("graph_drag_met_date", "style"),

    Input('button_drag_met', 'n_clicks'),
    Input('drag_met_date', 'start_date'),
    Input('drag_met_date', 'end_date'),
    Input('graph_drag_met_date','figure'),
    Input('graph_drag_met_date','style')
)
def updateGraphDragMet(drag_met_n_clicks, drag_met_start_date, drag_met_end_date, 
                oldFigureKeyRate, oldStyleDragMet,
                ):
    figurDragMet = {}
    styleDragMet = oldStyleDragMet  # Изначально скрыт
    
    if 'button_drag_met' == ctx.triggered_id:
        if not drag_met_start_date or not drag_met_end_date:
            raise PreventUpdate  # Не обновляем график, если поля пустые

        dragMetFilename = f'{drag_met_start_date}-{drag_met_end_date}.xml'
        CB.get_drag_met_dynamic_xml(drag_met_start_date, drag_met_end_date)
        figurDragMet = GraphBuilder().make_graph_from_drag_met(dragMetFilename)
        styleDragMet = {'display': 'block'}

    return figurDragMet, styleDragMet

if __name__ == '__main__':
    app.run(debug=True)