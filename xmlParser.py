import pandas as pd
import os

class XmlParser():

    def __init__(self):
        self._cwd = os.getcwd()


    def parse_xml_file(self, filename, directory, method):
        path = f'{self._cwd}\{directory}\{filename}'
        xml = pd.read_xml(path,xpath=f'//{method}')
        return xml

    def parse_curse_on_date(self, filename):
        return self.parse_xml_file(filename,'curseOnDate','ValuteCursOnDate')
    
    def parse_dynamic_curse_on_date(self, filename):
        return self.parse_xml_file(filename,'curseDynamic','ValuteCursDynamic')

    def parse_drag_met_dynamic(self, filename):
        return self.parse_xml_file(filename,'dragMetDynamic','DrgMet')
    
    def parse_key_rate(self, filename):
        return self.parse_xml_file(filename,'keyRate','KR')
    
    def parse_enum_reuters_values(self, filename):
        return self.parse_xml_file(filename,'enumReutersValues','EnumValutes')
    
    
    def get_vname_vchar_vcommoncode(self):
        df = self.parse_enum_reuters_values('справочник по кодам валют.xml')
        return df[['Vname','VcharCode','VcommonCode']]
    
    def get_vname(self, vCommorCode=''):
        df = self.get_vname_vchar_vcommoncode()

        if (vCommorCode == ''):
            return None
        
        return df.loc[(df['VcommonCode'] == vCommorCode)]['Vname'].values[0]

    def get_common_code(self, vname = '', vchar = ''):
        df = self.get_vname_vchar_vcommoncode()

        if (vname == ''):
            return None
        
        return df.loc[(df['Vname'] == vname)]['VcommonCode'].values[0]
        

    def get_vnames(self):
        df = self.get_vname_vchar_vcommoncode()
        return df['Vname'].values.tolist()

    def get_drag_met(self, filename):
        df = self.parse_drag_met_dynamic(filename)
        return df
    