from enum import Enum
from Endpoint import Endpoint

class OpenMeteoEndpoint(Enum, metaclass=Endpoint):
    FORECAST = 1
    HISTORICAL = 2

    @property
    def host(self): 
        if self.value == 1:
            return "api.open-meteo.com"
        if self.value == 2:
            return "archive-api.open-meteo.com"
        
    @property
    def path(self):
        if self.value == 1:
            return "/v1/forecast"
        if self.value == 2:
            return "/v1/archive"
        
    @property
    def url(self):
        return f"https://{self.host}{self.path}"
        
    @property
    def method(self):
        if self.value == 1:
            return 'GET'
        if self.value == 2:
            return 'GET'
