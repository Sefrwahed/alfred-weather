import requests
from datetime import datetime

from alfred.modules.api.a_base_widget import ABaseWidget
from alfred.modules.api.view_components import AParagraph

from .alfred_weather import AlfredWeather

class AlfredWeatherWidget(ABaseWidget):
    def callback(self):
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Cairo&units=metric&appid=7e73695b9106e411858e94e01532d30d")
        json_data = r.json()

        self.forecast = {
            'date_time': datetime.fromtimestamp(json_data['dt']).strftime("%a, %d"),
            'max_temp' : int(json_data['main']['temp_min']),
            'min_temp' : int(json_data['main']['temp_max']),
            'icon'     : json_data['weather'][0]['icon'][0:-1],
            'status'   : json_data['weather'][0]['description']
        }

    def construct_view(self):
        self.title = self.forecast["date_time"]
        self.content.append(AParagraph("Max: {}°C".format(self.forecast["max_temp"])))
        self.content.append(AParagraph("Min: {}°C".format(self.forecast["min_temp"])))
        self.content.append(AParagraph(self.forecast["status"]))
        self.image_url = AlfredWeather.image_link_for_weather_description(self.forecast["icon"])
        self.title_on_image = True