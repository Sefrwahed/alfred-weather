from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.a_heading import AHeading
from alfred.modules.api.a_ready_template import AReadyTemplate
from datetime import datetime
import requests
import os


class AlfredWeather(ABaseModule):

    def __init__(self, *args, **kwargs):
        ABaseModule.__init__(self,*args,**kwargs)
        self.forecast_data=[]

    def callback(self):
        r = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?q=Cairo&appid=7e73695b9106e411858e94e01532d30d")
        json_data = r.json()

        for i in range(json_data['cnt']):
            tmp={'date_time' : datetime.fromtimestamp(json_data["list"][i]['dt']).strftime("%a, %d"),
                 'max_temp'  : int(json_data["list"][i]['temp']['day'] - 273.15),
                 'min_temp'  : int(json_data["list"][i]['temp']['night'] - 273.15),
                 'status'    : json_data["list"][i]['weather'][0]['description']
                 }
            self.forecast_data.append(tmp)


    def construct_view(self):

        view = AReadyTemplate(self.forecast_data,
        os.path.dirname(os.path.abspath(__file__)),
        'weather.html'
        )
        self.add_component(view)
