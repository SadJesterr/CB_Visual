import pandas as pd
from xmlParser import XmlParser
import plotly.express as px

class GraphBuilder:
    def __init__(self):
        pass

    def make_graph_from_curse(self,filename='', vCode=''):
        df = XmlParser().parse_dynamic_curse_on_date(filename=filename)

        vName = XmlParser().get_vname(vCode)
                
        data = df[['CursDate','Vcurs']]
        fig = px.line(data, x='CursDate', y='Vcurs', title=vName)

        # Настраиваем легенду
        fig.update_layout(
            title = vName,
            xaxis_title = 'Дата',
            yaxis_title = 'Курс'
        )

        return fig
    

    def make_graph_from_key_rate(self,filename=''):
        df = XmlParser().parse_key_rate(filename=filename)
                
        titleName = 'Динамика ключевой ставки'
        data = df[['DT','Rate']]
        fig = px.line(data, x='DT', y='Rate', title=titleName)


        # Настраиваем легенду
        fig.update_layout(
            title = titleName,
            xaxis_title = 'Дата',
            yaxis_title = 'Значение'
        )

        return fig

    def make_graph_from_drag_met(self, filename=''):
        df = XmlParser().parse_drag_met_dynamic(filename=filename)
                
        titleName = 'Динамика стоимости'

        fig = px.line(df, x='DateMet', y='price', color='CodMet', title=titleName)


        fig.update_layout(
            title = titleName,
            xaxis_title = 'Дата',
            yaxis_title = 'Значение'
        )

        return fig
    
