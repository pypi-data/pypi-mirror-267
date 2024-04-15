from .enums import *
from requests_html import HTMLSession
import os

class SecLoad:
    def __init__(self, APIKey: str):
        self.APIKey = APIKey
        self.URL = "https://secload.scriptlang.com"
        self.session = HTMLSession()
        
    def CreateScript(self, script_name: str, source: str, sourcetype: ScriptType):
        if self.APIKey:
            data={
                "Key": self.APIKey,
                "ScriptName": script_name
            }
            if sourcetype.value == 1:
                data["Source"] = source
            else:
                if os.path.exists(source):
                    with open(source) as file:
                        data["Source"] = file.read()
                else:
                    raise Exception(f"File '{source}' does not exist.")
            
            response = self.session.post(self.URL+"/secload/publicapi/CreateScript", json=data)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")
        
    def RemoveScript(self, script_name: str):
        if self.APIKey:
            response = self.session.post(self.URL+"/secload/publicapi/RemoveScript", json={
                "Key": self.APIKey,
                "ScriptName": script_name,
            })
            
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")
        
    def OverwriteScript(self, script_name: str, source: str, sourcetype: ScriptType):
        if self.APIKey:
            data={
                "Key": self.APIKey,
                "ScriptName": script_name
            }
            if sourcetype.value == 1:
                data["Source"] = source
            else:
                if os.path.exists(source):
                    with open(source) as file:
                        data["Source"] = file.read()
                else:
                    raise Exception(f"File '{source}' does not exist.")
                
            response = self.session.post(self.URL+"/secload/publicapi/OverwriteScript", json=data)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")
        
    def ListScripts(self):
        if self.APIKey:
            response = self.session.post(self.URL+"/secload/publicapi/ListScripts", json={
                "Key": self.APIKey,
            })
            
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")
        
    def GenerateKey(self, script_name: str, username: str="username", time: int=5):
        if self.APIKey:
            response = self.session.post(self.URL+"/secload/publicapi/GenerateKey", json={
                "Key": self.APIKey,
                "ScriptName": script_name,
                "Username": username,
                "Time": time
            })
            
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")
        
    def GetScriptSource(self, script_name: str, sourcetype: ScriptType):
        if self.APIKey:
            data={
                "Key": self.APIKey,
                "ScriptName": script_name
            }
            if sourcetype.value == 1:
                data["Type"] = "text"
            else:
                data["Type"] = "file"
                
            response = self.session.post(self.URL+"/secload/publicapi/GetScriptSource", json=data)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"ERROR {response.status_code} - {response.text}")
        else:
            raise Exception("API Key has not been defined. Create a new API key at https://secload.scriptlang.com/docs")