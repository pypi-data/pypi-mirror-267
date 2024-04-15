
from datetime import datetime
import json
from xmlrpc.client import boolean
import requests
import pandas as pd
from typing import NewType
EconDataList = NewType('EconDataList', list['EconData'])
LoginResponse = NewType('LoginResponse','LoginResponse')
class DataFeedAdaptor:   
    base_url='https://marketwatch.cogencis.com/v2/staging/analyticsapi/api/v2/'
    local_base_url='http://localhost:5051/api/v2/'
    isConnected:boolean=False;
    token=None
    expiry=None
    headers={
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': '*/* ','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept-Language' : 'en-US,en;q=0.9,hi;q=0.8',
            'Accept-Encoding': 'gzip,deflate,br',
            'Referer': 'https://marketwatch.cogencis.com',
            }  
    def __init__(self):
        self
        
    def login(self,username,password) -> LoginResponse:
        self.username=username
        self.password=password
        
        url = f"{self.base_url}login"        
        payload={'username':self.username, 'password':self.password}
      
        response = requests.post(url, data=json.dumps(payload),headers=self.headers)
        
        if response.status_code == 200:
            self.isConnected=True
            resp=response.json();      
            if(resp['sucess']):
                self.token = resp['token']
                self.expiry= resp['expiry']
                self.headers['Authorization']=f"Bearer {self.token}"  
                
            return LoginResponse(resp)
      
        else:
            return response            
        
    def get_econ_timeseries(self,indicators:str,as_dataframe:boolean=True)->EconDataList:
        url = f"{self.base_url}econ/eventhistory?events={indicators}&ccy=USD"        
        response = requests.get(url,headers=self.headers)
        output=[]
        if response.status_code == 200:
            json_data = response.json()['response']
            
            for obj in json_data:
                output.append(EconData(obj,as_dataframe))
               
            return CogResponse(True,"",output)

            
        else:
            return CogResponse(False,"Falied",response) 
            #return response;

    def get_financials(self,isin):
        qs=f"isin={isin}"
        response =self.get_command("equity/financials",qs)        
        if response.status_code==200:
            json_data=response.json()['response'];
            return CogResponse(True,"Sucess",json_data)        

    def get_timeseries(self,symbol:str,fields:str='open,high,low,close,volume,date,time',
    timescale:int=1440,pageSize:int=250,direction:str='backward',start:str=None,end:str=None,as_dataframe:boolean=True):        
        qs=f"symbol={symbol}&fields={fields}&timescale={timescale}&pageSize={pageSize}&direction={direction}"
        if start!=None:
            qs = f"{qs}&&from={start}"
        
        if end!=None:
            qs = f"{qs}&&to={end}"
        
        response =self.get_command("timeseries",qs)   
        if(response.status_code==200):
            resp = response.json()            
            respdata = resp['response']['data']
            outdata=[]
            for snap in respdata:
                outdata.append(MarketData(snap))                        

            #resp["response"]=outdata
            return CogResponse(True,"Sucess",outdata)
        else:
             return CogResponse(False,"Falied",response) 
            
             
    def get_snapshot(self,symbol:str,fields:str='name,last,time,date',as_dataframe:boolean=True):        
        qs =f"symbol={symbol}&fields={fields}"
        response =self.get_command("snapshot",qs)       
        
        if response.status_code==200:
            resp =response.json()
            if as_dataframe:
                resp['response'] =pd.DataFrame(resp['response']['data'])
            else:
                resp['response'] =resp['response']['data']

            return CogResponse(True,"Sucess",resp['response'])
        else:
            return CogResponse(False,"Falied",response) 
        

    def get_command(self,route:str,querystring:str):
        url = f"{self.local_base_url}{route}?{querystring}"     
        response = requests.get(url,headers=self.headers)   
        return response
        

class EconData:
    def __init__(self, data,as_dataframe=False):        
        self.baseunit=data['baseunit'];
        self.country=data['country'];
        self.countryCode=data['countryCode'];
        self.frequency=data['frequency'];
        self.name=data['name'];            
        
        if as_dataframe:
            self.series = pd.DataFrame(data['series'])
        else:
            self.series=data['series']    
class MarketData:
    def __init__(self, data,as_dataframe=False):        
        self.symbol=data['symbol'];

        if as_dataframe:
            self.series = pd.DataFrame(data['data'])
        else:
            self.series=data['data']

class CogResponse:
    def __init__(self,status,message,data):        
        self.status=status
        self.message=message
        self.response = data

class LoginResponse:
    def __init__(self, data):       
        self.status=data['sucess']        
        self.response =data   
