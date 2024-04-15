
from datetime import datetime
import json
from xmlrpc.client import boolean
import requests
import pandas as pd

class DataFeedAdaptor:   
    base_url='https://marketwatch.cogencis.com/v2/staging/analyticsapi/api/v2/'
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
        
    def login(self,username,password) -> None:
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

        
    def get_econ_history(self,codes,as_dataframe=False):
        url = f"{self.base_url}econ/eventhistory?events={codes}&ccy=USD"        
        response = requests.get(url,headers=self.headers)
        output=[]
        if response.status_code == 200:
            json_data = response.json()['response']
            
            for obj in json_data:
                output.append(EconData(obj,as_dataframe))
               
            return output                
        else:
            return response;


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
        
class LoginResponse:
    def __init__(self, data):       
        self.status=data['sucess']        
        self.response =data   
