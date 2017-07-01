from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.view_components import ACard, AParagraph, ARow, AColumn
from datetime import datetime
import requests
import os


class AlfredWeather(ABaseModule):

    def __init__(self, *args, **kwargs):
        ABaseModule.__init__(self,*args,**kwargs)
        self.forecast_data=[]

    def callback(self):
        r = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?q=Cairo&units=metric&appid=7e73695b9106e411858e94e01532d30d")
        json_data = r.json()
        print(json_data)
        for i in range(json_data['cnt']):
            tmp={'date_time' : datetime.fromtimestamp(json_data["list"][i]['dt']).strftime("%a, %d"),
                 'max_temp'  : int(json_data["list"][i]['temp']['day']),
                 'min_temp'  : int(json_data["list"][i]['temp']['night']),
                 'icon'      : json_data["list"][i]['weather'][0]['icon'][0:-1],
                 'status'    : json_data["list"][i]['weather'][0]['description']
                 }
            self.forecast_data.append(tmp)

    def construct_view(self):
        row = ARow()

        for d in self.forecast_data:
            row.add_to_content(AColumn(6, ACard(
                d["date_time"],
                AParagraph("Max: {}°C".format(d["max_temp"])),
                AParagraph("Min: {}°C".format(d["min_temp"])),
                AParagraph(d["status"]),
                image_url=self.image_link_for_weather_description(d['icon']),
                title_on_image=True
            )))

        self.add_component(row)

    @classmethod
    def image_link_for_weather_description(self, icon_num):
        link_dict = {
            "09": "http://7bna.net/images/rainy-day-pictures/rainy-day-pictures-6.jpg",
            "10": "http://7bna.net/images/rainy-day-pictures/rainy-day-pictures-6.jpg",
            "01": "https://i.ytimg.com/vi/BQxBh-Oen1w/maxresdefault.jpg",
            "50": "http://img06.deviantart.net/ad0a/i/2012/333/a/9/a_foggy_day_by_festung1-d5mihmt.jpg"
        }

        return link_dict.get(icon_num, "http://cdn.digital-photo-secrets.com/images/flickr/5886837597_43db2672b6.jpg")