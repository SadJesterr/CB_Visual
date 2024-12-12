import requests
import os

class WebCbr():
    def __init__(self):
        self._url = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx'
        self._path = os.getcwd()
        self._localPath = ''

    def get_xml(self, SOAPAction, body):
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": SOAPAction
        }

        soap_request=f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            {f'{body}'}
        </soap:Body>
        </soap:Envelope>"""

        xml = self.post_request(
            soap_request=soap_request, 
            headers=headers)

        return xml


    def make_folder_if_not_exists(self, nameFolder):
        self._localPath = f'{self._path}/{nameFolder}'
        os.makedirs(self._localPath, exist_ok=True)

    def file_is_exist(self, path):
        return os.path.exists(path=path)

    def save_to_file(self, data, date, method):
        self.make_folder_if_not_exists(method)
        filepath = f"{self._localPath}/{date}.xml"

        if self.file_is_exist(filepath):
            print(f'Файл {date} в директории {method} уже существует')
            return None

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)
            print(f'Создан файл {date} в директории {method}')


    def post_request(self, soap_request,headers):
        response = requests.post(url=self._url, 
                                 data=soap_request, 
                                 headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None


    def get_curse_on_date_xml(self, date):
        soapAction = "http://web.cbr.ru/GetCursOnDateXML"
        body = f'''<GetCursOnDateXML xmlns="http://web.cbr.ru/">
            <On_date>{date}</On_date>
            </GetCursOnDateXML>'''

        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=date,
                method='curseOnDate')
            

    # valutaCode - VcommonCode
    def get_curse_dynamic_xml(self, startTime, endTime, valutaCode):  
        soapAction = "http://web.cbr.ru/GetCursDynamic"
        body = f'''<GetCursDynamic xmlns="http://web.cbr.ru/">
            <FromDate>{startTime}</FromDate>
            <ToDate>{endTime}</ToDate>
            <ValutaCode>{valutaCode}</ValutaCode>
            </GetCursDynamic>'''

        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=f'{valutaCode}-{startTime}-{endTime}',
                method='curseDynamic')


    def get_key_rate_xml(self, startTime, endTime):
        soapAction = "http://web.cbr.ru/KeyRateXML"

        body = f'''<KeyRateXML xmlns="http://web.cbr.ru/">
            <fromDate>{startTime}</fromDate>
            <ToDate>{endTime}</ToDate>
            </KeyRateXML>'''
        
        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=f'{startTime}-{endTime}',
                method='keyRate')
            

    def get_drag_met_dynamic_xml(self, startTime, endTime):
        soapAction = "http://web.cbr.ru/DragMetDynamicXML"
        body = f'''<DragMetDynamicXML xmlns="http://web.cbr.ru/">
            <fromDate>{startTime}</fromDate>
            <ToDate>{endTime}</ToDate>
            </DragMetDynamicXML>'''

        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=f'{startTime}-{endTime}',
                method='dragMetDynamic')

    def get_enum_values_xml(self):
        soapAction = "http://web.cbr.ru/EnumValutesXML"
        body = f'''<EnumValutesXML xmlns="http://web.cbr.ru/">
            <Seld>true</Seld>
            </EnumValutesXML>'''

        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=f'справочник по  кодам валют',
                method='enumValues')
            

    def get_enum__reuters_values_xml(self):
        soapAction = "http://web.cbr.ru/EnumValutesXML"
        body = '<EnumReutersValutesXML xmlns="http://web.cbr.ru/" />'

        xml = self.get_xml(SOAPAction=soapAction, body=body)

        if xml is not None:
            self.save_to_file(
                data=xml, 
                date=f'справочник по кодам валют',
                method='enumReutersValues')
            
